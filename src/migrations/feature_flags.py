"""Módulo para gerenciar feature flags da migração."""
from enum import Enum
from typing import Dict, Optional
import json
from pathlib import Path

class MigrationFlag(Enum):
    """Flags para controle da migração."""
    USE_NEW_FORMS = "use_new_forms"
    IDENTIFICATION_MIGRATED = "identification_migrated"
    PROCESS_DETAILS_MIGRATED = "process_details_migrated"
    BUSINESS_RULES_MIGRATED = "business_rules_migrated"
    AUTOMATION_GOALS_MIGRATED = "automation_goals_migrated"
    SYSTEMS_MIGRATED = "systems_migrated"
    DATA_MIGRATED = "data_migrated"
    STEPS_MIGRATED = "steps_migrated"
    RISKS_MIGRATED = "risks_migrated"
    DOCUMENTATION_MIGRATED = "documentation_migrated"

class FeatureFlagManager:
    """Gerenciador de feature flags."""
    
    def __init__(self, config_file: str = "config/feature_flags.json"):
        """
        Inicializa o gerenciador.
        
        Args:
            config_file: Caminho para arquivo de configuração
        """
        self.config_file = Path(config_file)
        self._flags: Dict[str, bool] = {}
        self._load_flags()
    
    def _load_flags(self) -> None:
        """Carrega flags do arquivo de configuração."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self._flags = json.load(f)
        else:
            # Inicializa com todos os flags desativados
            self._flags = {flag.value: False for flag in MigrationFlag}
            self._save_flags()
    
    def _save_flags(self) -> None:
        """Salva flags no arquivo de configuração."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self._flags, f, indent=4)
    
    def is_enabled(self, flag: MigrationFlag) -> bool:
        """
        Verifica se um flag está ativado.
        
        Args:
            flag: Flag a ser verificado
            
        Returns:
            bool: True se ativado, False caso contrário
        """
        return self._flags.get(flag.value, False)
    
    def enable(self, flag: MigrationFlag) -> None:
        """
        Ativa um flag.
        
        Args:
            flag: Flag a ser ativado
        """
        self._flags[flag.value] = True
        self._save_flags()
    
    def disable(self, flag: MigrationFlag) -> None:
        """
        Desativa um flag.
        
        Args:
            flag: Flag a ser desativado
        """
        self._flags[flag.value] = False
        self._save_flags()
    
    def reset_all(self) -> None:
        """Reseta todos os flags para desativado."""
        self._flags = {flag.value: False for flag in MigrationFlag}
        self._save_flags()
    
    @property
    def status(self) -> Dict[str, bool]:
        """Retorna status atual de todos os flags."""
        return self._flags.copy() 