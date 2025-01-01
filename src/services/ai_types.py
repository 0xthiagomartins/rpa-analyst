"""Tipos de dados para o serviço de IA."""
from typing import TypedDict, List, Dict, Optional, Literal

class FormData(TypedDict):
    """Dados base para formulários."""
    form_id: str
    is_valid: bool
    has_changes: bool
    data: dict

class AIResponse(TypedDict):
    """Resposta da IA."""
    description: str
    forms_data: Dict[str, FormData]
    suggestions: List[str]
    validation: List[str]

class SuggestionPreview(TypedDict):
    """Preview de sugestões."""
    original: str
    improved: str
    changes: List[str]
    confidence: float
    form_previews: Dict[str, 'FormPreview']

class FormPreview(TypedDict):
    """Preview de mudanças no formulário."""
    form_id: str
    changes: List['Change']
    validation: List[str]

class Change(TypedDict):
    """Mudança sugerida."""
    field: str
    old_value: Optional[str]
    new_value: str
    type: Literal['add', 'modify', 'remove']
    confidence: float 