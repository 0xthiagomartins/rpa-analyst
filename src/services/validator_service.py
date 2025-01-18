"""Serviço de validação de sugestões da IA."""
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from utils.logger import Logger

@dataclass
class ValidationResult:
    """Resultado da validação."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ValidatorService:
    """Serviço para validação de sugestões da IA."""
    
    def __init__(self):
        """Inicializa o serviço."""
        self.logger = Logger()

    def validate_suggestions(self, suggestions: Dict[str, Any]) -> ValidationResult:
        """
        Valida sugestões da IA.
        
        Args:
            suggestions: Sugestões a serem validadas
            
        Returns:
            ValidationResult com resultado da validação
        """
        errors = []
        warnings = []

        # Valida estrutura básica
        if not self._validate_structure(suggestions, errors):
            return ValidationResult(False, errors, warnings)

        # Valida conteúdo
        self._validate_content(suggestions, errors, warnings)
        
        # Valida relacionamentos
        self._validate_relationships(suggestions, errors, warnings)

        return ValidationResult(len(errors) == 0, errors, warnings)

    def _validate_structure(self, suggestions: Dict[str, Any], errors: List[str]) -> bool:
        """Valida estrutura básica das sugestões."""
        required_fields = {'description', 'forms_data', 'suggestions', 'validation'}
        
        for field in required_fields:
            if field not in suggestions:
                errors.append(f"Campo obrigatório ausente: {field}")
                return False
                
        if not isinstance(suggestions['forms_data'], dict):
            errors.append("forms_data deve ser um dicionário")
            return False
            
        return True

    def _validate_content(self, suggestions: Dict[str, Any], errors: List[str], warnings: List[str]):
        """Valida conteúdo das sugestões."""
        # Valida descrição
        if len(suggestions['description']) < 10:
            warnings.append("Descrição muito curta")
            
        # Valida dados dos formulários
        for form_id, form_data in suggestions['forms_data'].items():
            if not isinstance(form_data, dict):
                errors.append(f"Dados inválidos para formulário {form_id}")
                continue
                
            if 'data' not in form_data:
                errors.append(f"Campo 'data' ausente em {form_id}")

    def _validate_relationships(self, suggestions: Dict[str, Any], errors: List[str], warnings: List[str]):
        """Valida relacionamentos entre dados dos formulários."""
        forms_data = suggestions['forms_data']
        
        # Valida referências entre formulários
        if 'steps' in forms_data and 'systems' in forms_data:
            self._validate_steps_systems_relationship(
                forms_data['steps'].get('data', {}),
                forms_data['systems'].get('data', {}),
                errors
            )

    def _validate_steps_systems_relationship(
        self,
        steps_data: Dict[str, Any],
        systems_data: Dict[str, Any],
        errors: List[str]
    ):
        """Valida relacionamento entre passos e sistemas."""
        systems = {s['name'] for s in systems_data.get('systems', [])}
        
        for step in steps_data.get('steps', []):
            if 'system' in step and step['system'] not in systems:
                errors.append(
                    f"Sistema '{step['system']}' referenciado no passo '{step.get('name', '')}' "
                    "não está definido"
                ) 