"""Módulo para mapeamento de dados entre formatos."""
from typing import Dict, Any, Optional

class DataMapper:
    """Classe para mapear dados entre formatos antigo e novo."""
    
    @staticmethod
    def map_identification_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do IdentificationForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        return {
            "process_name": old_data.get("name", ""),
            "process_id": old_data.get("id", ""),
            "department": old_data.get("department", ""),
            "owner": old_data.get("owner", ""),
            "participants": old_data.get("participants", []),
            "creation_date": old_data.get("created_at", ""),
            "last_update": old_data.get("updated_at", ""),
            "status": old_data.get("status", "draft")
        }
    
    @staticmethod
    def map_process_details_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do ProcessDetailsForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        return {
            "description": old_data.get("description", ""),
            "objective": old_data.get("objective", ""),
            "scope": {
                "in_scope": old_data.get("scope_in", []),
                "out_scope": old_data.get("scope_out", [])
            },
            "process_type": old_data.get("type", "manual"),
            "frequency": {
                "execution_frequency": old_data.get("frequency", "daily"),
                "volume": old_data.get("volume", 0),
                "peak_times": old_data.get("peak_times", [])
            },
            "complexity": {
                "level": old_data.get("complexity", "medium"),
                "factors": old_data.get("complexity_factors", [])
            },
            "dependencies": {
                "upstream": old_data.get("dependencies_upstream", []),
                "downstream": old_data.get("dependencies_downstream", [])
            },
            "additional_info": old_data.get("additional_info", "")
        }
    
    @staticmethod
    def map_business_rules_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do BusinessRulesForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia regras de negócio
        business_rules = []
        for rule in old_data.get("rules", []):
            business_rules.append({
                "rule_id": rule.get("id", ""),
                "description": rule.get("description", ""),
                "rule_type": rule.get("type", "general"),
                "priority": rule.get("priority", "medium"),
                "exceptions": rule.get("exceptions", [])
            })
        
        # Mapeia validações
        validations = []
        for validation in old_data.get("validations", []):
            validations.append({
                "field_name": validation.get("field", ""),
                "validation_rule": validation.get("rule", ""),
                "error_message": validation.get("error_message", "")
            })
        
        # Mapeia cálculos
        calculations = []
        for calc in old_data.get("calculations", []):
            calculations.append({
                "calculation_name": calc.get("name", ""),
                "formula": calc.get("formula", ""),
                "description": calc.get("description", "")
            })
        
        # Mapeia condições
        conditions = []
        for cond in old_data.get("conditions", []):
            conditions.append({
                "condition": cond.get("if", ""),
                "action": cond.get("then", ""),
                "description": cond.get("description", "")
            })
        
        return {
            "business_rules": business_rules,
            "validations": validations,
            "calculations": calculations,
            "conditions": conditions
        }
    
    @staticmethod
    def map_automation_goals_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do AutomationGoalsForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia objetivos de automação
        automation_goals = []
        for goal in old_data.get("goals", []):
            metrics = goal.get("metrics", {})
            automation_goals.append({
                "goal_id": goal.get("id", ""),
                "description": goal.get("description", ""),
                "category": goal.get("category", "general"),
                "metrics": {
                    "current_value": metrics.get("current", ""),
                    "target_value": metrics.get("target", ""),
                    "unit": metrics.get("unit", "")
                }
            })
        
        # Mapeia benefícios
        benefits = []
        for benefit in old_data.get("benefits", []):
            benefits.append({
                "benefit_type": benefit.get("type", ""),
                "description": benefit.get("description", ""),
                "value": benefit.get("value", ""),
                "unit": benefit.get("currency", benefit.get("unit", "")),
                "timeframe": benefit.get("timeframe", "")
            })
        
        # Mapeia restrições
        constraints = []
        for constraint in old_data.get("constraints", []):
            constraints.append({
                "constraint_type": constraint.get("type", ""),
                "description": constraint.get("description", ""),
                "impact_level": constraint.get("impact", "medium")
            })
        
        # Mapeia timeline
        timeline = old_data.get("timeline", {})
        implementation_timeline = {
            "start_date": timeline.get("start_date", ""),
            "end_date": timeline.get("end_date", ""),
            "milestones": []
        }
        
        for milestone in timeline.get("milestones", []):
            implementation_timeline["milestones"].append({
                "milestone_name": milestone.get("name", ""),
                "target_date": milestone.get("date", ""),
                "deliverables": milestone.get("deliverables", [])
            })
        
        return {
            "automation_goals": automation_goals,
            "benefits": benefits,
            "constraints": constraints,
            "success_criteria": old_data.get("success_criteria", []),
            "priority_level": old_data.get("priority", "medium"),
            "implementation_timeline": implementation_timeline
        }
    
    @staticmethod
    def map_systems_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do SystemsForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia sistemas
        systems = []
        for system in old_data.get("systems", []):
            access = system.get("access", {})
            availability = system.get("availability", {})
            
            systems.append({
                "system_id": system.get("id", ""),
                "system_name": system.get("name", ""),
                "system_type": system.get("type", ""),
                "version": system.get("version", ""),
                "modules": system.get("modules", []),
                "access_details": {
                    "access_type": access.get("type", ""),
                    "credentials_type": access.get("credentials", ""),
                    "permissions": access.get("permissions", [])
                },
                "availability": {
                    "service_hours": availability.get("hours", ""),
                    "sla": availability.get("sla", ""),
                    "maintenance_window": availability.get("maintenance_window", "")
                }
            })
        
        # Mapeia integrações
        integrations = []
        for integration in old_data.get("integrations", []):
            integrations.append({
                "source_system": integration.get("source", ""),
                "target_system": integration.get("target", ""),
                "integration_type": integration.get("type", ""),
                "sync_frequency": integration.get("frequency", ""),
                "data_elements": integration.get("data_flow", []),
                "integration_requirements": integration.get("requirements", [])
            })
        
        # Mapeia fluxos de dados
        data_flows = []
        for flow in old_data.get("data_flows", []):
            data_flows.append({
                "flow_name": flow.get("name", ""),
                "description": flow.get("description", ""),
                "involved_systems": flow.get("systems", []),
                "sync_frequency": flow.get("frequency", ""),
                "daily_volume": flow.get("volume", "")
            })
        
        # Mapeia requisitos técnicos
        technical_requirements = []
        for req in old_data.get("technical_requirements", []):
            technical_requirements.append({
                "requirement_category": req.get("category", ""),
                "description": req.get("description", ""),
                "priority_level": req.get("priority", "medium")
            })
        
        return {
            "systems": systems,
            "integrations": integrations,
            "data_flows": data_flows,
            "technical_requirements": technical_requirements
        }
    
    @staticmethod
    def map_data_form_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do DataForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia inputs
        data_inputs = []
        for input_data in old_data.get("inputs", []):
            quality = input_data.get("quality_metrics", {})
            data_inputs.append({
                "input_id": input_data.get("id", ""),
                "input_name": input_data.get("name", ""),
                "data_type": input_data.get("type", "unstructured"),
                "file_format": input_data.get("format", ""),
                "data_source": input_data.get("source", ""),
                "field_definitions": [
                    {
                        "field_name": field.get("name", ""),
                        "data_type": field.get("type", ""),
                        "is_required": field.get("required", False),
                        "validation_rule": field.get("validation", "")
                    }
                    for field in input_data.get("fields", [])
                ],
                "daily_volume": input_data.get("volume", ""),
                "quality_metrics": {
                    "accuracy_rate": quality.get("accuracy", ""),
                    "completeness_rate": quality.get("completeness", "")
                }
            })
        
        # Mapeia outputs
        data_outputs = []
        for output_data in old_data.get("outputs", []):
            data_outputs.append({
                "output_id": output_data.get("id", ""),
                "output_name": output_data.get("name", ""),
                "data_type": output_data.get("type", "unstructured"),
                "file_format": output_data.get("format", ""),
                "destination_system": output_data.get("destination", ""),
                "field_definitions": [
                    {
                        "field_name": field.get("name", ""),
                        "data_type": field.get("type", ""),
                        "is_required": field.get("required", False)
                    }
                    for field in output_data.get("fields", [])
                ],
                "output_frequency": output_data.get("frequency", "batch")
            })
        
        # Mapeia transformações
        data_transformations = []
        for transform in old_data.get("transformations", []):
            data_transformations.append({
                "transformation_id": transform.get("id", ""),
                "transformation_name": transform.get("name", ""),
                "description": transform.get("description", ""),
                "input_fields": transform.get("input_fields", []),
                "output_fields": transform.get("output_fields", []),
                "transformation_rules": transform.get("rules", [])
            })
        
        # Mapeia controles de qualidade
        quality = old_data.get("data_quality", {})
        monitoring = quality.get("monitoring", {})
        quality_controls = {
            "validation_rules": [
                {
                    "field_name": rule.get("field", ""),
                    "rule_definition": rule.get("rule", ""),
                    "severity_level": rule.get("severity", "warning")
                }
                for rule in quality.get("validation_rules", [])
            ],
            "monitoring_config": {
                "metrics": monitoring.get("metrics", []),
                "check_frequency": monitoring.get("frequency", "daily"),
                "alert_channels": monitoring.get("alerts", [])
            }
        }
        
        # Mapeia retenção
        retention = old_data.get("retention", {})
        storage = retention.get("storage", {})
        data_retention = {
            "retention_period": retention.get("period", "1 year"),
            "archival_policy": retention.get("policy", ""),
            "storage_locations": {
                "active_data": storage.get("active", "database"),
                "archived_data": storage.get("archive", "")
            }
        }
        
        return {
            "data_inputs": data_inputs,
            "data_outputs": data_outputs,
            "data_transformations": data_transformations,
            "quality_controls": quality_controls,
            "data_retention": data_retention
        }
    
    @staticmethod
    def map_steps_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do StepsForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia passos
        process_steps = []
        for step in old_data.get("steps", []):
            dependencies = step.get("dependencies", {})
            process_steps.append({
                "step_id": step.get("id", ""),
                "step_name": step.get("name", ""),
                "description": step.get("description", ""),
                "step_type": step.get("type", "manual"),
                "assigned_role": step.get("role", ""),
                "time_estimate": step.get("estimated_time", ""),
                "step_inputs": step.get("inputs", []),
                "step_outputs": step.get("outputs", []),
                "required_systems": step.get("systems", []),
                "execution_instructions": step.get("instructions", []),
                "validation_points": step.get("validations", []),
                "dependencies": {
                    "previous_steps": dependencies.get("previous", []),
                    "next_steps": dependencies.get("next", [])
                }
            })
        
        # Mapeia fluxo do processo
        flow = old_data.get("flow", {})
        process_flow = {
            "initial_step": flow.get("start_step", ""),
            "final_step": flow.get("end_step", ""),
            "parallel_execution": flow.get("parallel_steps", []),
            "conditional_execution": flow.get("conditional_steps", [])
        }
        
        # Mapeia papéis
        process_roles = []
        for role in old_data.get("roles", []):
            process_roles.append({
                "role_name": role.get("name", ""),
                "role_responsibilities": role.get("responsibilities", []),
                "required_skills": role.get("skills", [])
            })
        
        # Mapeia métricas
        metrics = old_data.get("metrics", {})
        process_metrics = {
            "total_processing_time": metrics.get("total_time", ""),
            "manual_processing_time": metrics.get("manual_time", ""),
            "automated_processing_time": metrics.get("automated_time", ""),
            "number_of_handoffs": metrics.get("handoffs", 0)
        }
        
        return {
            "process_steps": process_steps,
            "process_flow": process_flow,
            "process_roles": process_roles,
            "process_metrics": process_metrics
        }
    
    @staticmethod
    def map_risks_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do RisksForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia riscos identificados
        identified_risks = []
        for risk in old_data.get("risks", []):
            mitigation = risk.get("mitigation_plan", {})
            identified_risks.append({
                "risk_id": risk.get("id", ""),
                "description": risk.get("description", ""),
                "risk_category": risk.get("category", "general"),
                "probability_level": risk.get("probability", "low"),
                "impact_level": risk.get("impact", "low"),
                "severity_level": risk.get("severity", "low"),
                "affected_areas": risk.get("affected_areas", []),
                "existing_controls": risk.get("current_controls", []),
                "mitigation_strategy": {
                    "planned_actions": mitigation.get("actions", []),
                    "responsible_party": mitigation.get("responsible", ""),
                    "target_date": mitigation.get("deadline", ""),
                    "status": mitigation.get("status", "planned")
                }
            })
        
        # Mapeia matriz de avaliação de riscos
        matrix = old_data.get("risk_matrix", {})
        risk_assessment_matrix = {
            "probability_scale": matrix.get("probability_levels", ["low", "medium", "high"]),
            "impact_scale": matrix.get("impact_levels", ["low", "medium", "high"]),
            "severity_calculation": matrix.get("severity_mapping", {})
        }
        
        # Mapeia monitoramento de riscos
        monitoring = old_data.get("monitoring", {})
        reporting = monitoring.get("reporting", {})
        risk_monitoring = {
            "monitoring_frequency": monitoring.get("frequency", "monthly"),
            "responsible_party": monitoring.get("responsible", ""),
            "monitoring_metrics": monitoring.get("metrics", []),
            "reporting_config": {
                "report_format": reporting.get("format", ""),
                "report_recipients": reporting.get("recipients", [])
            }
        }
        
        # Mapeia planos de contingência
        contingency_plans = []
        for plan in old_data.get("contingency_plans", []):
            contingency_plans.append({
                "associated_risk": plan.get("risk_id", ""),
                "trigger_events": plan.get("trigger_conditions", []),
                "response_actions": plan.get("actions", []),
                "required_resources": plan.get("resources_needed", []),
                "recovery_target": plan.get("recovery_time_objective", "")
            })
        
        return {
            "identified_risks": identified_risks,
            "risk_assessment_matrix": risk_assessment_matrix,
            "risk_monitoring": risk_monitoring,
            "contingency_plans": contingency_plans
        }
    
    @staticmethod
    def map_documentation_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapeia dados do DocumentationForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato
        """
        # Mapeia documentação do processo
        doc = old_data.get("process_documentation", {})
        process_documentation = {
            "document_version": doc.get("version", "1.0"),
            "last_updated": doc.get("last_update", ""),
            "document_author": doc.get("author", ""),
            "document_status": doc.get("status", "draft"),
            "content_sections": []
        }
        
        # Mapeia seções da documentação
        for section in doc.get("sections", []):
            process_documentation["content_sections"].append({
                "section_id": section.get("id", ""),
                "section_title": section.get("title", ""),
                "section_content": section.get("content", ""),
                "section_attachments": [
                    {
                        "file_name": attachment.get("name", ""),
                        "file_type": attachment.get("type", ""),
                        "file_url": attachment.get("url", ""),
                        "description": attachment.get("description", "")
                    }
                    for attachment in section.get("attachments", [])
                ]
            })
        
        # Mapeia materiais de treinamento
        training_materials = []
        for material in old_data.get("training_materials", []):
            training_materials.append({
                "material_id": material.get("id", ""),
                "material_title": material.get("title", ""),
                "file_type": material.get("type", ""),
                "file_format": material.get("format", ""),
                "file_url": material.get("url", ""),
                "target_audience": material.get("target_audience", []),
                "version": material.get("version", "1.0")
            })
        
        # Mapeia histórico de alterações
        change_history = []
        for change in old_data.get("change_history", []):
            change_history.append({
                "change_date": change.get("date", ""),
                "change_author": change.get("author", ""),
                "change_type": change.get("type", ""),
                "change_description": change.get("description", "")
            })
        
        # Mapeia referências
        references = []
        for ref in old_data.get("references", []):
            references.append({
                "reference_title": ref.get("title", ""),
                "reference_type": ref.get("type", ""),
                "reference_url": ref.get("url", ""),
                "description": ref.get("description", "")
            })
        
        # Mapeia ciclo de revisão
        review = old_data.get("review_cycle", {})
        review_cycle = {
            "review_frequency": review.get("frequency", "annual"),
            "last_review_date": review.get("last_review", ""),
            "next_review_date": review.get("next_review", ""),
            "review_team": review.get("reviewers", [])
        }
        
        return {
            "process_documentation": process_documentation,
            "training_materials": training_materials,
            "change_history": change_history,
            "references": references,
            "review_cycle": review_cycle
        } 