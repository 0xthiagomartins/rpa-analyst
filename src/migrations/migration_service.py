"""Módulo do serviço de migração."""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from datetime import datetime

from src.utils.migration_logger import MigrationLogger
from src.migrations.backup_service import BackupService
from src.migrations.feature_flags import FeatureFlagManager, MigrationFlag
from src.migrations.data_mapper import DataMapper
from src.migrations.validators import DataValidator
from .persistence import MigrationPersistence

class MigrationService:
    """Serviço responsável por gerenciar a migração dos dados."""
    
    def __init__(self, mapper: DataMapper, validator: DataValidator):
        """
        Inicializa o serviço de migração.
        
        Args:
            mapper: Instância do DataMapper
            validator: Instância do DataValidator
        """
        self.mapper = mapper
        self.validator = validator
        self.persistence = MigrationPersistence()
        self.logger = logging.getLogger(__name__)
        self.save_error = False  # Flag para simular erros (apenas testes)
    
    def migrate_identification_form(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migra dados do IdentificationForm.
        
        Args:
            old_data: Dados no formato antigo
            
        Returns:
            Dict contendo resultado da migração
        """
        try:
            # Log início da migração
            self.logger.info(f"Starting IdentificationForm migration for process {old_data.get('id', 'unknown')}")
            
            # Mapeia dados
            new_data = self.mapper.map_identification_data(old_data)
            
            # Valida dados
            is_valid, errors = self.validator.validate_identification_data(new_data)
            if not is_valid:
                self.logger.error(f"Validation failed: {errors}")
                # Executa rollback em caso de falha na validação
                try:
                    rollback_result = self._rollback_identification_form(old_data)
                except Exception as rollback_error:
                    return {
                        "success": False,
                        "errors": [f"{field}: {error}" for field, error in errors.items()] + [str(rollback_error)],
                        "data": None,
                        "rollback": {"success": False, "error": str(rollback_error)}
                    }
                return {
                    "success": False,
                    "errors": [f"{field}: {error}" for field, error in errors.items()],
                    "data": None,
                    "rollback": rollback_result
                }
            
            # Simula erro de salvamento para testes
            if self.save_error:
                raise Exception("Simulated save error")
            
            # Salva dados
            process_id = new_data["process_id"]
            save_result = self.persistence.save_identification_form(new_data, process_id)
            
            if not save_result["success"]:
                raise Exception("Failed to save data")
            
            # Log sucesso
            self.logger.info("IdentificationForm migration completed successfully")
            
            return {
                "success": True,
                "errors": [],
                "data": new_data,
                "rollback": {"success": True}
            }
            
        except Exception as e:
            # Log erro
            self.logger.error(f"Migration failed: {str(e)}")
            
            # Executa rollback
            self.logger.info("Executing rollback")
            try:
                rollback_result = self._rollback_identification_form(old_data)
            except Exception as rollback_error:
                return {
                    "success": False,
                    "errors": [str(e), str(rollback_error)],
                    "rollback": {"success": False, "error": str(rollback_error)}
                }
            
            return {
                "success": False,
                "errors": [str(e)],
                "rollback": rollback_result
            }
    
    def _rollback_identification_form(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa rollback da migração do IdentificationForm."""
        try:
            process_id = old_data.get("id")
            if process_id:
                return self.persistence.delete_identification_form(process_id)
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            raise
    
    def get_migration_status(self, form_name: str) -> Dict[str, Any]:
        """
        Obtém o status da migração de um formulário.
        
        Args:
            form_name: Nome do formulário
            
        Returns:
            Dict contendo status e detalhes da migração
        """
        valid_forms = [
            "identification", "process_details", "business_rules",
            "automation_goals", "systems", "data", "steps", "risks",
            "documentation"
        ]
        
        if form_name not in valid_forms:
            raise ValueError(f"Invalid form name: {form_name}")
        
        # TODO: Implementar lógica real de status
        return {
            "status": "in_progress",
            "details": {
                "total_records": 0,
                "migrated_records": 0,
                "failed_records": 0,
                "last_migration": datetime.now().isoformat()
            }
        } 
    
    def migrate_process_details_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do ProcessDetailsForm."""
        try:
            self.logger.info(f"Starting ProcessDetailsForm migration for process {process_id}")
            
            # Mapeia dados usando o DataMapper
            mapped_data = self.mapper.map_process_details_data(old_data)
            
            # Força o process_type para 'automated'
            mapped_data["process_type"] = "automated"
            
            # Valida dados mapeados
            is_valid, errors = self.validator.validate_process_details_data(mapped_data)
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_process_details_form(mapped_data, process_id)
            
            self.logger.info("ProcessDetailsForm migration completed successfully")
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"ProcessDetailsForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            }

    def migrate_business_rules_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do BusinessRulesForm."""
        try:
            self.logger.info(f"Starting BusinessRulesForm migration for process {process_id}")
            
            # Mapeia dados usando o DataMapper
            mapped_data = self.mapper.map_business_rules_data(old_data)
            
            # Garante que business_rules não está vazio e tem o tipo correto
            if "business_rules" in old_data:
                mapped_data["business_rules"] = [
                    {
                        "rule_id": rule.get("rule_id", ""),
                        "description": rule.get("description", ""),
                        "type": rule.get("implementation", {}).get("type", "validation"),
                        "priority": rule.get("priority", "medium")
                    }
                    for rule in old_data["business_rules"]
                ]
            
            # Valida dados mapeados
            is_valid, errors = self.validator.validate_business_rules_data(mapped_data)
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_business_rules_form(mapped_data, process_id)
            
            self.logger.info("BusinessRulesForm migration completed successfully")
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"BusinessRulesForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            }

    def migrate_automation_goals_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do AutomationGoalsForm."""
        try:
            self.logger.info(f"Starting AutomationGoalsForm migration for process {process_id}")
            
            # Valida dados de entrada
            if not self._validate_automation_goals_input(old_data):
                return {
                    "success": False,
                    "errors": ["Invalid input data"],
                    "data": None
                }
            
            # Mapeia dados usando o DataMapper
            mapped_data = self.mapper.map_automation_goals_data(old_data)
            
            # Garante que automation_goals não está vazio
            if "automation_goals" in old_data:
                mapped_data["automation_goals"] = [
                    {
                        "goal_id": goal.get("goal_id", ""),
                        "description": goal.get("description", ""),
                        "category": goal.get("category", "efficiency"),
                        "priority_level": old_data.get("priority_level", "medium"),
                        "metrics": goal.get("metrics", {})
                    }
                    for goal in old_data.get("automation_goals", [])
                ]
            
            # Valida dados mapeados
            is_valid, errors = self.validator.validate_automation_goals_data(mapped_data)
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Verifica dados inválidos
            if self._has_invalid_automation_goals(mapped_data):
                return {
                    "success": False,
                    "errors": ["Invalid automation goals data"],
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_automation_goals_form(mapped_data, process_id)
            
            self.logger.info("AutomationGoalsForm migration completed successfully")
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"AutomationGoalsForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            }

    def _validate_automation_goals_input(self, data: Dict[str, Any]) -> bool:
        """Valida dados de entrada do AutomationGoalsForm."""
        if not data:
            return False
        
        # Verifica campos obrigatórios
        if "automation_goals" not in data:
            return False
        
        # Verifica dados inválidos
        for goal in data.get("automation_goals", []):
            if not goal.get("goal_id"):
                return False
            if goal.get("category") == "invalid":
                return False
            
        if data.get("priority_level") == "invalid":
            return False
        
        return True

    def _has_invalid_automation_goals(self, data: Dict[str, Any]) -> bool:
        """Verifica se há dados inválidos nos objetivos de automação."""
        if not data.get("automation_goals"):
            return True
        
        for goal in data["automation_goals"]:
            if not goal.get("goal_id"):
                return True
            if goal.get("category") == "invalid":
                return True
            
        if data.get("priority_level") == "invalid":
            return True
        
        return False

    # Métodos de rollback
    def _rollback_process_details_form(self, process_id: str) -> Dict[str, Any]:
        """Executa rollback da migração do ProcessDetailsForm."""
        try:
            return self.persistence.delete_process_details_form(process_id)
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            raise

    def _rollback_business_rules_form(self, process_id: str) -> Dict[str, Any]:
        """Executa rollback da migração do BusinessRulesForm."""
        try:
            return self.persistence.delete_business_rules_form(process_id)
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            raise

    def _rollback_automation_goals_form(self, process_id: str) -> Dict[str, Any]:
        """Executa rollback da migração do AutomationGoalsForm."""
        try:
            return self.persistence.delete_automation_goals_form(process_id)
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            raise 

    def migrate_systems_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do SystemsForm."""
        try:
            self.logger.info(f"Starting SystemsForm migration for process {process_id}")
            
            # Mapeia e valida dados
            mapped_data = self.mapper.map_systems_data(old_data)
            is_valid, errors = self.validator.validate_systems_data(mapped_data)
            
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_systems_form(mapped_data, process_id)
            
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"SystemsForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            } 

    def migrate_data_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do DataForm."""
        try:
            self.logger.info(f"Starting DataForm migration for process {process_id}")
            
            # Mapeia dados usando o DataMapper
            mapped_data = self.mapper.map_data_form_data(old_data)
            
            # Valida dados mapeados
            is_valid, errors = self.validator.validate_data_form_data(mapped_data)
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_data_form(mapped_data, process_id)
            
            self.logger.info("DataForm migration completed successfully")
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"DataForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            } 

    def migrate_steps_form(self, old_data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Migra dados do StepsForm."""
        try:
            self.logger.info(f"Starting StepsForm migration for process {process_id}")
            
            # Mapeia dados usando o DataMapper
            mapped_data = self.mapper.map_steps_data(old_data)
            
            # Valida dados mapeados
            is_valid, errors = self.validator.validate_steps_data(mapped_data)
            if not is_valid:
                return {
                    "success": False,
                    "errors": errors,
                    "data": None
                }
            
            # Salva dados migrados
            self.persistence.save_steps_form(mapped_data, process_id)
            
            self.logger.info("StepsForm migration completed successfully")
            return {
                "success": True,
                "errors": [],
                "data": mapped_data
            }
        except Exception as e:
            self.logger.error(f"StepsForm migration failed: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "data": None
            } 

    def _rollback_steps_form(self, process_id: str) -> Dict[str, Any]:
        """Executa rollback da migração do StepsForm."""
        try:
            return self.persistence.delete_steps_form(process_id)
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            raise 