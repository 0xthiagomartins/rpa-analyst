"""Módulo para validação de dados migrados."""
import re
from datetime import datetime
from typing import Dict, Any, Tuple, List

class DataValidator:
    """Classe para validar dados migrados."""
    
    def __init__(self):
        """Inicializa o validador."""
        self.valid_statuses = ["draft", "in_review", "approved", "archived"]
        self.valid_process_types = ["manual", "automated", "hybrid"]
        self.valid_frequencies = ["daily", "weekly", "monthly", "quarterly", "yearly"]
        self.valid_complexities = ["low", "medium", "high"]
        self.valid_priorities = ["low", "medium", "high", "critical"]
        self.valid_rule_types = ["validation", "calculation", "business", "technical"]
        self.valid_data_types = ["string", "number", "date", "boolean", "object", "array"]
        self.valid_severity_levels = ["info", "warning", "error", "critical"]
        
    def validate_identification_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """
        Valida dados do IdentificationForm.
        
        Args:
            data: Dados a serem validados
            
        Returns:
            Tuple[bool, Dict]: (resultado da validação, erros encontrados)
        """
        errors = {}
        
        # Valida campos obrigatórios
        required_fields = ["process_name", "process_id", "department", "owner"]
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"Field {field} is required"
        
        # Valida formato do process_id
        if data.get("process_id"):
            if not re.match(r"^PROC-\d{3,}$", data["process_id"]):
                errors["process_id"] = "Invalid process ID format (should be PROC-XXX)"
        
        # Valida datas
        for date_field in ["creation_date", "last_update"]:
            if date_value := data.get(date_field):
                try:
                    datetime.strptime(date_value, "%Y-%m-%d")
                except ValueError:
                    errors[date_field] = f"Invalid date format for {date_field}"
        
        # Valida status
        if status := data.get("status"):
            if status not in self.valid_statuses:
                errors["status"] = f"Invalid status. Must be one of: {', '.join(self.valid_statuses)}"
        
        # Valida participantes
        if participants := data.get("participants"):
            if not isinstance(participants, list):
                errors["participants"] = "Must be a list of participants"
        
        return len(errors) == 0, errors
    
    def _validate_date(self, date_str: str) -> bool:
        """Valida formato de data."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _validate_required_fields(self, data: Dict[str, Any], required: List[str]) -> Dict[str, str]:
        """Valida campos obrigatórios."""
        errors = {}
        for field in required:
            if not data.get(field):
                errors[field] = f"Field {field} is required"
        return errors 
    
    def validate_process_details_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do ProcessDetailsForm."""
        errors = {}
        
        # Campos obrigatórios
        errors.update(self._validate_required_fields(data, ["description", "objective"]))
        
        # Valida tipo do processo
        if process_type := data.get("process_type"):
            if process_type not in self.valid_process_types:
                errors["process_type"] = f"Invalid process type. Must be one of: {', '.join(self.valid_process_types)}"
        
        # Valida frequência
        frequency = data.get("frequency", {}).get("execution_frequency")
        if frequency and frequency not in self.valid_frequencies:
            errors["frequency"] = f"Invalid frequency. Must be one of: {', '.join(self.valid_frequencies)}"
        
        # Valida complexidade
        complexity = data.get("complexity", {}).get("level")
        if complexity and complexity not in self.valid_complexities:
            errors["complexity"] = f"Invalid complexity level. Must be one of: {', '.join(self.valid_complexities)}"
        
        return len(errors) == 0, errors
    
    def validate_business_rules_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do BusinessRulesForm."""
        errors = {}
        
        # Valida regras de negócio
        for i, rule in enumerate(data.get("business_rules", [])):
            if not rule.get("rule_id"):
                errors[f"business_rules[{i}].rule_id"] = "Rule ID is required"
            if not rule.get("description"):
                errors[f"business_rules[{i}].description"] = "Rule description is required"
            if rule_type := rule.get("rule_type"):
                if rule_type not in self.valid_rule_types:
                    errors[f"business_rules[{i}].rule_type"] = f"Invalid rule type. Must be one of: {', '.join(self.valid_rule_types)}"
        
        return len(errors) == 0, errors
    
    def validate_data_form_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do DataForm."""
        errors = {}
        
        # Valida inputs
        for i, input_data in enumerate(data.get("data_inputs", [])):
            if not input_data.get("input_id"):
                errors[f"data_inputs[{i}].input_id"] = "Input ID is required"
            if not input_data.get("name"):
                errors[f"data_inputs[{i}].name"] = "Input name is required"
            if not input_data.get("type"):
                errors[f"data_inputs[{i}].type"] = "Input type is required"
            
            # Valida campos
            for j, field in enumerate(input_data.get("fields", [])):
                if not field.get("name"):
                    errors[f"data_inputs[{i}].fields[{j}].name"] = "Field name is required"
                if field_type := field.get("type"):
                    if field_type not in self.valid_data_types:
                        errors[f"data_inputs[{i}].fields[{j}].type"] = f"Invalid data type"
        
        # Valida outputs
        for i, output_data in enumerate(data.get("data_outputs", [])):
            if not output_data.get("output_id"):
                errors[f"data_outputs[{i}].output_id"] = "Output ID is required"
            if not output_data.get("name"):
                errors[f"data_outputs[{i}].name"] = "Output name is required"
            if not output_data.get("destination"):
                errors[f"data_outputs[{i}].destination"] = "Destination system is required"
        
        # Valida transformações
        for i, transform in enumerate(data.get("transformations", [])):
            if not transform.get("id"):
                errors[f"transformations[{i}].id"] = "Transformation ID is required"
            if not transform.get("name"):
                errors[f"transformations[{i}].name"] = "Transformation name is required"
            if not transform.get("input_fields"):
                errors[f"transformations[{i}].input_fields"] = "Input fields are required"
            if not transform.get("output_fields"):
                errors[f"transformations[{i}].output_fields"] = "Output fields are required"
        
        return len(errors) == 0, errors
    
    def validate_risks_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do RisksForm."""
        errors = {}
        
        # Valida riscos identificados
        for i, risk in enumerate(data.get("identified_risks", [])):
            # Campos obrigatórios
            if not risk.get("risk_id"):
                errors[f"identified_risks[{i}].risk_id"] = "Risk ID is required"
            if not risk.get("description"):
                errors[f"identified_risks[{i}].description"] = "Risk description is required"
            
            # Valida níveis
            for level_field in ["probability_level", "impact_level", "severity_level"]:
                if level := risk.get(level_field):
                    if level not in ["low", "medium", "high", "critical"]:
                        errors[f"identified_risks[{i}].{level_field}"] = f"Invalid {level_field}"
            
            # Valida estratégia de mitigação
            strategy = risk.get("mitigation_strategy", {})
            if not strategy.get("planned_actions"):
                errors[f"identified_risks[{i}].mitigation_strategy.planned_actions"] = "Planned actions are required"
            if target_date := strategy.get("target_date"):
                if not self._validate_date(target_date):
                    errors[f"identified_risks[{i}].mitigation_strategy.target_date"] = "Invalid date format"
        
        # Valida matriz de avaliação
        matrix = data.get("risk_assessment_matrix", {})
        for scale in ["probability_scale", "impact_scale"]:
            if not matrix.get(scale):
                errors[f"risk_assessment_matrix.{scale}"] = f"{scale} is required"
        
        return len(errors) == 0, errors
    
    def validate_automation_goals_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do AutomationGoalsForm."""
        errors = {}
        
        # Valida objetivos de automação
        for i, goal in enumerate(data.get("automation_goals", [])):
            if not goal.get("goal_id"):
                errors[f"automation_goals[{i}].goal_id"] = "Goal ID is required"
            if not goal.get("description"):
                errors[f"automation_goals[{i}].description"] = "Goal description is required"
            
            # Valida métricas
            metrics = goal.get("metrics", {})
            if not metrics.get("current_value"):
                errors[f"automation_goals[{i}].metrics.current_value"] = "Current value is required"
            if not metrics.get("target_value"):
                errors[f"automation_goals[{i}].metrics.target_value"] = "Target value is required"
        
        # Valida prioridade
        if priority := data.get("priority_level"):
            if priority not in self.valid_priorities:
                errors["priority_level"] = f"Invalid priority level. Must be one of: {', '.join(self.valid_priorities)}"
        
        return len(errors) == 0, errors
    
    def validate_systems_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do SystemsForm."""
        errors = {}
        
        # Valida sistemas
        if not data.get("systems"):
            errors["systems"] = "At least one system is required"
        
        for i, system in enumerate(data.get("systems", [])):
            if not system.get("system_id"):
                errors[f"systems[{i}].system_id"] = "System ID is required"
            if not system.get("system_name"):
                errors[f"systems[{i}].system_name"] = "System name is required"
            if not system.get("system_type"):
                errors[f"systems[{i}].system_type"] = "System type is required"
            
            # Valida acesso
            access = system.get("access_details", {})
            if not access.get("access_type"):
                errors[f"systems[{i}].access_details.access_type"] = "Access type is required"
        
        # Valida integrações
        for i, integration in enumerate(data.get("integrations", [])):
            if not integration.get("source_system"):
                errors[f"integrations[{i}].source_system"] = "Source system is required"
            if not integration.get("target_system"):
                errors[f"integrations[{i}].target_system"] = "Target system is required"
            if not integration.get("integration_type"):
                errors[f"integrations[{i}].integration_type"] = "Integration type is required"
        
        return len(errors) == 0, errors
    
    def validate_steps_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do StepsForm."""
        errors = {}
        
        # Valida passos do processo
        if not data.get("process_steps"):
            errors["process_steps"] = "At least one process step is required"
        
        for i, step in enumerate(data.get("process_steps", [])):
            if not step.get("step_id"):
                errors[f"process_steps[{i}].step_id"] = "Step ID is required"
            if not step.get("step_name"):
                errors[f"process_steps[{i}].step_name"] = "Step name is required"
            if not step.get("description"):
                errors[f"process_steps[{i}].description"] = "Step description is required"
            if step_type := step.get("step_type"):
                if step_type not in ["manual", "automated", "hybrid"]:
                    errors[f"process_steps[{i}].step_type"] = "Invalid step type"
            
            # Valida dependências
            deps = step.get("dependencies", {})
            if not isinstance(deps.get("previous_steps", []), list):
                errors[f"process_steps[{i}].dependencies.previous_steps"] = "Previous steps must be a list"
            if not isinstance(deps.get("next_steps", []), list):
                errors[f"process_steps[{i}].dependencies.next_steps"] = "Next steps must be a list"
        
        # Valida fluxo do processo
        flow = data.get("process_flow", {})
        if not flow.get("initial_step"):
            errors["process_flow.initial_step"] = "Initial step is required"
        if not flow.get("final_step"):
            errors["process_flow.final_step"] = "Final step is required"
        
        return len(errors) == 0, errors
    
    def validate_documentation_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Valida dados do DocumentationForm."""
        errors = {}
        
        # Valida documentação do processo
        doc = data.get("process_documentation", {})
        if not doc.get("document_version"):
            errors["process_documentation.document_version"] = "Document version is required"
        
        # Valida status do documento
        if status := doc.get("document_status"):
            if status not in self.valid_statuses:
                errors["process_documentation.document_status"] = f"Invalid document status"
        
        # Valida data de atualização
        if last_updated := doc.get("last_updated"):
            if not self._validate_date(last_updated):
                errors["process_documentation.last_updated"] = "Invalid date format"
        
        # Valida seções de conteúdo
        for i, section in enumerate(doc.get("content_sections", [])):
            if not section.get("section_id"):
                errors[f"process_documentation.content_sections[{i}].section_id"] = "Section ID is required"
            if not section.get("section_title"):
                errors[f"process_documentation.content_sections[{i}].section_title"] = "Section title is required"
        
        # Valida materiais de treinamento
        for i, material in enumerate(data.get("training_materials", [])):
            if not material.get("material_id"):
                errors[f"training_materials[{i}].material_id"] = "Material ID is required"
            if not material.get("material_title"):
                errors[f"training_materials[{i}].material_title"] = "Material title is required"
            if not material.get("file_type"):
                errors[f"training_materials[{i}].file_type"] = "File type is required"
        
        return len(errors) == 0, errors 