"""Módulo do serviço de migração."""
from typing import Dict, Any, Optional, List
from pathlib import Path

from src.utils.migration_logger import MigrationLogger
from src.migrations.backup_service import BackupService
from src.migrations.feature_flags import FeatureFlagManager, MigrationFlag

class MigrationService:
    """Serviço responsável por gerenciar a migração dos dados."""
    
    def __init__(self):
        """Inicializa o serviço de migração."""
        self.logger = MigrationLogger()
        self.backup_service = BackupService()
        self.feature_flags = FeatureFlagManager()
        
    def start_migration(self, form_name: str, data: Dict[str, Any]) -> bool:
        """
        Inicia o processo de migração para um formulário.
        
        Args:
            form_name: Nome do formulário
            data: Dados a serem migrados
            
        Returns:
            bool: True se migração foi bem sucedida
        """
        try:
            self.logger.info(f"Starting migration for {form_name}")
            
            # Cria backup antes da migração
            backup_file = self.backup_service.create_backup(form_name, data)
            if not backup_file:
                self.logger.error(f"Failed to create backup for {form_name}")
                return False
            
            # Mapeia dados para novo formato
            new_data = self._map_data(form_name, data)
            if not new_data:
                self.logger.error(f"Failed to map data for {form_name}")
                return False
            
            # Valida dados migrados
            if not self._validate_migration(form_name, new_data):
                self.logger.error(f"Validation failed for {form_name}")
                return False
            
            # Atualiza feature flag
            self._update_feature_flag(form_name)
            
            self.logger.info(f"Migration completed for {form_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during migration of {form_name}", e)
            return False
    
    def _map_data(self, form_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Mapeia dados do formato antigo para o novo.
        
        Args:
            form_name: Nome do formulário
            data: Dados no formato antigo
            
        Returns:
            Dict: Dados no novo formato ou None se falhar
        """
        try:
            # TODO: Implementar mapeamento específico para cada formulário
            mapping_methods = {
                "identification": self._map_identification_data,
                "process_details": self._map_process_details_data,
                "business_rules": self._map_business_rules_data,
                "automation_goals": self._map_automation_goals_data,
                "systems": self._map_systems_data,
                "data": self._map_data_form_data,
                "steps": self._map_steps_data,
                "risks": self._map_risks_data,
                "documentation": self._map_documentation_data
            }
            
            if form_name not in mapping_methods:
                raise ValueError(f"Unknown form: {form_name}")
                
            return mapping_methods[form_name](data)
            
        except Exception as e:
            self.logger.error(f"Error mapping data for {form_name}", e)
            return None
    
    def _validate_migration(self, form_name: str, data: Dict[str, Any]) -> bool:
        """
        Valida os dados migrados.
        
        Args:
            form_name: Nome do formulário
            data: Dados migrados
            
        Returns:
            bool: True se dados são válidos
        """
        # TODO: Implementar validação específica para cada formulário
        return True
    
    def _update_feature_flag(self, form_name: str) -> None:
        """
        Atualiza feature flag após migração bem sucedida.
        
        Args:
            form_name: Nome do formulário
        """
        flag_mapping = {
            "identification": MigrationFlag.IDENTIFICATION_MIGRATED,
            "process_details": MigrationFlag.PROCESS_DETAILS_MIGRATED,
            "business_rules": MigrationFlag.BUSINESS_RULES_MIGRATED,
            "automation_goals": MigrationFlag.AUTOMATION_GOALS_MIGRATED,
            "systems": MigrationFlag.SYSTEMS_MIGRATED,
            "data": MigrationFlag.DATA_MIGRATED,
            "steps": MigrationFlag.STEPS_MIGRATED,
            "risks": MigrationFlag.RISKS_MIGRATED,
            "documentation": MigrationFlag.DOCUMENTATION_MIGRATED
        }
        
        if form_name in flag_mapping:
            self.feature_flags.enable(flag_mapping[form_name])
    
    def get_migration_status(self) -> Dict[str, bool]:
        """
        Retorna status atual da migração.
        
        Returns:
            Dict: Status de migração de cada formulário
        """
        return self.feature_flags.status
    
    def rollback_migration(self, form_name: str, backup_file: Path) -> bool:
        """
        Reverte uma migração usando backup.
        
        Args:
            form_name: Nome do formulário
            backup_file: Arquivo de backup
            
        Returns:
            bool: True se rollback foi bem sucedido
        """
        try:
            self.logger.info(f"Starting rollback for {form_name}")
            
            # Restaura dados do backup
            data = self.backup_service.restore_backup(backup_file)
            if not data:
                self.logger.error(f"Failed to restore backup for {form_name}")
                return False
            
            # Desativa feature flag
            flag_mapping = {
                "identification": MigrationFlag.IDENTIFICATION_MIGRATED,
                "process_details": MigrationFlag.PROCESS_DETAILS_MIGRATED,
                "business_rules": MigrationFlag.BUSINESS_RULES_MIGRATED,
                "automation_goals": MigrationFlag.AUTOMATION_GOALS_MIGRATED,
                "systems": MigrationFlag.SYSTEMS_MIGRATED,
                "data": MigrationFlag.DATA_MIGRATED,
                "steps": MigrationFlag.STEPS_MIGRATED,
                "risks": MigrationFlag.RISKS_MIGRATED,
                "documentation": MigrationFlag.DOCUMENTATION_MIGRATED
            }
            
            if form_name in flag_mapping:
                self.feature_flags.disable(flag_mapping[form_name])
            
            self.logger.info(f"Rollback completed for {form_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during rollback of {form_name}", e)
            return False 