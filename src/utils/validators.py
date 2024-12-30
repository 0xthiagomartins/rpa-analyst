"""Módulo de validadores para o sistema."""
from typing import Dict, List, Tuple, Any
from src.utils.context import AppContext
import re
from src.utils.config_constants import UI_CONFIG

class ValidationError:
    """Classe para representar erros de validação."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

class FormValidator:
    """Classe para validação de formulários."""
    
    def __init__(self):
        self.config = AppContext.get_config()
    
    def validate_form(self, data: Dict[str, Any], section: str) -> List[ValidationError]:
        """Valida os dados do formulário para uma seção específica."""
        errors = []
        required_fields = self.config.get_required_fields(section)
        
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(
                    ValidationError(
                        field=field,
                        message=f"O campo '{self.get_field_label(field)}' é obrigatório."
                    )
                )
        
        return errors
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Valida campos obrigatórios específicos."""
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        return len(missing_fields) == 0, missing_fields
    
    def get_field_label(self, field: str) -> str:
        """Retorna o rótulo para um campo específico."""
        return self.config.get_field_label(field)
    
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

# Funções de validação específicas
def validate_process_name(name: str) -> bool:
    """Valida o nome do processo."""
    if not name or not name.strip():
        return False
    
    if len(name) > UI_CONFIG['MAX_NAME_LENGTH']:
        return False
    
    return True

def validate_process_description(description: str) -> bool:
    """Valida a descrição do processo."""
    if not description or not description.strip():
        return False
    
    if len(description) > UI_CONFIG['MAX_DESCRIPTION_LENGTH']:
        return False
    
    return True

def validate_diagram(diagram: str) -> bool:
    """Valida a sintaxe do diagrama Mermaid."""
    if not diagram or not isinstance(diagram, str):
        return False
        
    # Remove espaços em branco extras e quebras de linha
    diagram = diagram.strip()
    
    # Validações básicas de sintaxe
    required_elements = [
        'graph',  # Deve ter a declaração do tipo de gráfico
        '[',      # Deve ter pelo menos um nó
        ']',      # Fechamento do nó
        '-->'     # Deve ter pelo menos uma conexão
    ]
    
    for element in required_elements:
        if element not in diagram:
            return False
            
    # Verifica se há nós sem conexão ou conexões incompletas
    lines = [line.strip() for line in diagram.split('\n') if line.strip()]
    for line in lines:
        if '-->' in line:
            parts = line.split('-->')
            if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                return False
                
        if '[' in line and ']' in line and '-->' not in line:
            if not any(line in other_line for other_line in lines if '-->' in other_line):
                return False
                
    return True

def validate_required_fields(data: Dict[str, Any], required: List[str]) -> bool:
    """Valida se todos os campos obrigatórios estão preenchidos."""
    if not data or not required:
        return False
    
    for field in required:
        if field not in data:
            return False
        
        value = data[field]
        if isinstance(value, str) and not value.strip():
            return False
        elif value is None:
            return False
    
    return True