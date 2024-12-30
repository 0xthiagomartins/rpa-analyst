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
        frequency_data = old_data.get("frequency", {})
        if isinstance(frequency_data, str):
            frequency_data = {
                "execution_frequency": frequency_data,
                "volume": old_data.get("volume", 0),
                "peak_times": old_data.get("peak_times", [])
            }
        
        complexity_data = old_data.get("complexity", {})
        if isinstance(complexity_data, str):
            complexity_data = {
                "level": complexity_data.lower(),
                "factors": old_data.get("complexity_factors", [])
            }
        
        return {
            "description": old_data.get("description", ""),
            "objective": old_data.get("objective", ""),
            "process_type": old_data.get("type", "manual"),
            "frequency": {
                "execution_frequency": frequency_data.get("execution_frequency", "daily"),
                "volume": int(frequency_data.get("volume", 0)),
                "peak_times": old_data.get("peak_times", [])
            },
            "complexity": {
                "level": complexity_data.get("level", "medium").lower(),
                "factors": complexity_data.get("factors", [])
            },
            "scope": {
                "in_scope": old_data.get("scope_in", []),
                "out_scope": old_data.get("scope_out", [])
            },
            "dependencies": {
                "upstream": old_data.get("dependencies_upstream", []),
                "downstream": old_data.get("dependencies_downstream", [])
            },
            "additional_info": old_data.get("additional_info", "")
        }
    
    @staticmethod
    def map_business_rules_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia dados do BusinessRulesForm."""
        rules = []
        validations = []
        calculations = []
        conditions = []
        
        # Mapeia regras do formato antigo (limitado a 2)
        for rule in old_data.get("rules", [])[:2]:
            rules.append({
                "rule_id": rule.get("id", ""),
                "description": rule.get("description", ""),
                "rule_type": rule.get("type", "general").lower(),
                "priority": rule.get("priority", "medium").lower(),
                "implementation": rule.get("implementation", {}),
                "exceptions": rule.get("exceptions", [])
            })
        
        # Mapeia condições
        for condition in old_data.get("conditions", []):
            conditions.append({
                "condition_id": condition.get("id", ""),
                "description": condition.get("description", ""),
                "condition_type": condition.get("type", ""),
                "evaluation_criteria": condition.get("criteria", ""),
                "condition": condition.get("condition", "amount > 1000"),
                "action": condition.get("action", "require_approval")
            })
        
        # Mapeia validações antigas
        for validation in old_data.get("validations", []):
            validation_rule = {
                "rule_id": validation.get("id", "BR" + str(len(validations) + 1).zfill(3)),
                "description": validation.get("error_message", ""),
                "rule_type": "validation",
                "priority": "medium",
                "implementation": {
                    "field": validation.get("field", ""),
                    "rule": validation.get("rule", "")
                },
                "exceptions": []
            }
            validations.append({
                "field_name": validation.get("field", ""),
                "validation_rule": validation.get("rule", ""),
                "error_message": validation.get("error_message", "")
            })
        
        # Mapeia cálculos
        for calc in old_data.get("calculations", []):
            calculations.append({
                "calculation_id": calc.get("id", ""),
                "calculation_name": calc.get("name", ""),
                "description": calc.get("description", ""),
                "formula": calc.get("formula", "")
            })
        
        return {
            "rules": rules,
            "business_rules": rules,
            "validations": validations,
            "calculations": calculations,
            "conditions": conditions,
            "dependencies": old_data.get("dependencies", [])
        }
    
    @staticmethod
    def map_automation_goals_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia dados do AutomationGoalsForm."""
        print("Input data:", old_data)  # Debug
        automation_goals = []
        
        for goal in old_data.get("goals", []):
            print("Processing goal:", goal)  # Debug
            automation_goals.append({
                "goal_id": goal.get("id", ""),
                "description": goal.get("description", ""),
                "category": goal.get("type", "general"),
                "priority_level": old_data.get("priority", "medium"),
                "metrics": {
                    "current_value": goal.get("metrics", {}).get("current", ""),
                    "target_value": goal.get("metrics", {}).get("target", ""),
                    "unit": goal.get("metrics", {}).get("unit", "")
                },
                "timeline": {
                    "start_date": "",
                    "end_date": "",
                    "milestones": []
                }
            })
        
        # Mapeia critérios de sucesso
        success_criteria = []
        for criteria in old_data.get("success_criteria", []):
            if isinstance(criteria, dict):
                success_criteria.append({
                    "criteria_id": criteria.get("id", ""),
                    "description": criteria.get("description", ""),
                    "measurement_method": criteria.get("measurement", ""),
                    "target_value": criteria.get("target", "")
                })
            else:
                success_criteria.append(str(criteria))
        
        return {
            "automation_goals": automation_goals,
            "priority_level": old_data.get("priority", "medium"),
            "benefits": [
                {
                    "benefit_type": benefit.get("type", ""),
                    "description": benefit.get("description", ""),
                    "value": benefit.get("value", 0),
                    "currency": benefit.get("currency", "USD"),
                    "timeframe": benefit.get("timeframe", "yearly"),
                    "unit": benefit.get("currency", "USD")
                }
                for benefit in old_data.get("benefits", [])
            ],
            "dependencies": old_data.get("dependencies", []),
            "constraints": old_data.get("constraints", []),
            "success_criteria": success_criteria,
            "implementation_timeline": {
                "start_date": "",
                "end_date": "",
                "milestones": []
            }
        }
    
    @staticmethod
    def map_systems_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia dados do SystemsForm."""
        systems = []
        
        for system in old_data.get("systems", []):
            systems.append({
                "system_id": system.get("id", ""),
                "name": system.get("name", ""),
                "type": system.get("type", ""),
                "version": system.get("version", ""),
                "modules": system.get("modules", []),
                "access": {
                    "type": system.get("access", {}).get("type", ""),
                    "credentials": system.get("access", {}).get("credentials", ""),
                    "permissions": system.get("access", {}).get("permissions", [])
                },
                "availability": {
                    "hours": system.get("availability", {}).get("hours", ""),
                    "sla": system.get("availability", {}).get("sla", ""),
                    "maintenance_window": system.get("availability", {}).get("maintenance_window", "")
                }
            })
        
        return {
            "systems": systems,
            "integrations": [
                {
                    "source_system": integration.get("source", ""),
                    "target_system": integration.get("target", ""),
                    "integration_type": integration.get("type", ""),
                    "frequency": integration.get("frequency", ""),
                    "data_flows": integration.get("data_flow", [])
                }
                for integration in old_data.get("integrations", [])
            ],
            "technical_requirements": [
                {
                    "requirement_type": req.get("category", ""),
                    "description": req.get("description", ""),
                    "priority": req.get("priority", "medium")
                }
                for req in old_data.get("technical_requirements", [])
            ]
        }
    
    @staticmethod
    def map_data_form_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia dados do DataForm."""
        try:
            mapped_data = {
                "data_inputs": [],
                "data_outputs": [],
                "transformations": [],
                "data_quality": {
                    "validation_rules": [],
                    "quality_metrics": {},
                    "error_handling": {}
                }
            }

            # Mapeia inputs
            for input_data in old_data.get("data_inputs", []):
                mapped_input = {
                    "input_id": input_data.get("input_id", ""),
                    "name": input_data.get("name", ""),
                    "type": input_data.get("type", ""),
                    "format": input_data.get("format", ""),
                    "source": input_data.get("source", ""),
                    "fields": []
                }
                
                # Mapeia campos do input
                for field in input_data.get("fields", []):
                    mapped_field = {
                        "name": field.get("name", ""),
                        "type": field.get("type", ""),
                        "required": field.get("required", False),
                        "validation_rule": field.get("validation_rule", "")
                    }
                    mapped_input["fields"].append(mapped_field)
                    
                mapped_data["data_inputs"].append(mapped_input)

            # Mapeia outputs
            for output_data in old_data.get("data_outputs", []):
                mapped_output = {
                    "output_id": output_data.get("output_id", ""),
                    "name": output_data.get("name", ""),
                    "type": output_data.get("type", ""),
                    "format": output_data.get("format", ""),
                    "destination": output_data.get("destination", "")
                }
                mapped_data["data_outputs"].append(mapped_output)

            # Mapeia transformações
            for transform in old_data.get("transformations", []):
                mapped_transform = {
                    "id": transform.get("transformation_id", ""),
                    "name": transform.get("name", ""),
                    "description": transform.get("description", ""),
                    "input_fields": transform.get("input_fields", []),
                    "output_fields": transform.get("output_fields", []),
                    "rules": transform.get("rules", [])
                }
                mapped_data["transformations"].append(mapped_transform)

            # Mapeia qualidade de dados
            quality = old_data.get("data_quality", {})
            mapped_data["data_quality"] = {
                "validation_rules": quality.get("validation_rules", []),
                "quality_metrics": quality.get("quality_metrics", {}),
                "error_handling": quality.get("error_handling", {})
            }

            return mapped_data
        except Exception as e:
            raise ValueError(f"Failed to map data form data: {str(e)}")
    
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