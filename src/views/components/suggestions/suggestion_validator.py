"""Módulo para validação de sugestões."""
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from src.utils.logger import Logger
from src.views.components.suggestions.suggestions_buffer import SuggestionData

@dataclass
class ValidationResult:
    """Resultado da validação de uma sugestão."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class SuggestionValidator:
    """Validador de sugestões da IA."""
    
    def __init__(self):
        """Inicializa o validador."""
        self.logger = Logger()
    
    def validate_suggestion(self, suggestion: SuggestionData) -> ValidationResult:
        """
        Valida uma sugestão completa.
        
        Args:
            suggestion: Dados da sugestão a validar
            
        Returns:
            ValidationResult com resultado da validação
        """
        errors = []
        warnings = []
        
        # Valida estrutura básica
        if not self._validate_structure(suggestion.data):
            errors.append("Estrutura de dados inválida")
            return ValidationResult(False, errors, warnings)
        
        # Valida campos específicos do formulário
        form_errors = self._validate_form_fields(suggestion.form_id, suggestion.data)
        errors.extend(form_errors)
        
        # Valida consistência dos dados
        consistency_result = self._validate_consistency(suggestion.data)
        errors.extend(consistency_result[0])
        warnings.extend(consistency_result[1])
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_structure(self, data: Dict[str, Any]) -> bool:
        """Valida estrutura básica dos dados."""
        try:
            if not isinstance(data, dict):
                return False
            
            # Verifica campos obrigatórios comuns
            required = {"form_id", "data", "timestamp"}
            if not all(field in data for field in required):
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Erro na validação de estrutura: {str(e)}")
            return False
    
    def _validate_form_fields(self, form_id: str, data: Dict[str, Any]) -> List[str]:
        """Valida campos específicos do formulário."""
        errors = []
        
        # Extrai dados do formulário da estrutura aninhada
        form_data = data.get("data", {})
        
        # Mapeamento de validações específicas por formulário
        validators = {
            "identification": self._validate_identification,
            "process_details": self._validate_process_details,
            "business_rules": self._validate_business_rules,
            "systems": self._validate_systems,
        }
        
        # Executa validador específico se existir
        if validator := validators.get(form_id):
            form_errors = validator(form_data)
            errors.extend(form_errors)
        
        return errors
    
    def _validate_consistency(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Valida consistência geral dos dados."""
        errors = []
        warnings = []
        
        # Validações de consistência aqui
        # Por exemplo, verificar referências entre campos
        
        return errors, warnings
    
    # Validadores específicos por formulário
    def _validate_identification(self, data: Dict[str, Any]) -> List[str]:
        """Valida dados do formulário de identificação."""
        errors = []
        
        required = {"process_name", "responsible", "department"}
        for field in required:
            if not data.get(field):
                errors.append(f"Campo {field} é obrigatório")
        
        return errors
    
    def _validate_process_details(self, data: Dict[str, Any]) -> List[str]:
        """Valida dados do formulário de detalhes."""
        errors = []
        
        required = {"objective", "scope", "systems"}
        for field in required:
            if not data.get(field):
                errors.append(f"Campo {field} é obrigatório")
        
        return errors
    
    def _validate_business_rules(self, data: Dict[str, Any]) -> List[str]:
        """Valida dados do formulário de regras."""
        errors = []
        
        if "rules" not in data or not isinstance(data["rules"], list):
            errors.append("Lista de regras inválida")
        
        return errors 
    
    def _validate_systems(self, data: Dict[str, Any]) -> List[str]:
        """Valida dados do formulário de sistemas."""
        errors = []
        
        # Valida lista de sistemas
        if "systems" not in data or not isinstance(data["systems"], list):
            errors.append("Lista de sistemas inválida")
            return errors
            
        # Valida estrutura de cada sistema
        for i, system in enumerate(data["systems"]):
            if not isinstance(system, dict):
                errors.append(f"Sistema {i+1} tem formato inválido")
                continue
                
            # Campos obrigatórios para cada sistema
            required = {"name", "type", "access_type"}
            for field in required:
                if not system.get(field):
                    errors.append(f"Campo {field} é obrigatório para o sistema {i+1}")
        
        # Valida integrações se existirem
        if "integrations" in data:
            if not isinstance(data["integrations"], list):
                errors.append("Lista de integrações inválida")
            else:
                for i, integration in enumerate(data["integrations"]):
                    if not isinstance(integration, dict):
                        errors.append(f"Integração {i+1} tem formato inválido")
                        continue
                        
                    # Campos obrigatórios para cada integração
                    required = {"source", "target", "type"}
                    for field in required:
                        if not integration.get(field):
                            errors.append(f"Campo {field} é obrigatório para a integração {i+1}")
        
        return errors 