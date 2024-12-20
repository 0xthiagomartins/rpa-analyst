from typing import Dict, List, Tuple, Any
from src.utils.context import AppContext
import re

class ValidationError:
    """Classe para representar erros de validação."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

class FormValidator:
    """Classe para validação de formulários."""
    
    def __init__(self):
        self.config = AppContext.get_config()
    
    def validate_required_fields(self, data: Dict[str, str], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Valida campos obrigatórios."""
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not str(data.get(field, '')).strip():
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields

    def get_field_label(self, field_name: str) -> str:
        """Retorna o rótulo amigável para o campo."""
        return self.config.get_field_label(field_name)

    def validate_email(self, email: str) -> bool:
        """Valida formato de email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_length(self, text: str, min_length: int = 0, max_length: int = None) -> bool:
        """Valida comprimento do texto."""
        if max_length is None:
            return len(text.strip()) >= min_length
        return min_length <= len(text.strip()) <= max_length
    
    def validate_field_type(self, value: Any, expected_type: type) -> bool:
        """Valida tipo do campo."""
        return isinstance(value, expected_type)

    def validate_form(self, data: Dict[str, Any], section: str) -> List[ValidationError]:
        """Valida um formulário completo."""
        errors = []
        required_fields = self.config.get_required_fields(section)
        
        for field in required_fields:
            if field not in data or not str(data.get(field, '')).strip():
                label = self.get_field_label(field)
                errors.append(
                    ValidationError(field, f"O campo '{label}' é obrigatório.")
                )
        
        return errors