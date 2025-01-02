"""Módulo para gerenciar o buffer de sugestões."""
from typing import Dict, Any, Optional, List
import streamlit as st
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SuggestionBuffer:
    """Buffer de sugestões da IA."""
    timestamp: datetime
    description: str
    forms_data: Dict[str, Any]
    suggestions: List[str]
    validation: List[str]
    applied_to: List[str] = None

    @classmethod
    def from_response(cls, response: Dict[str, Any]) -> 'SuggestionBuffer':
        """Cria buffer a partir da resposta da IA."""
        return cls(
            timestamp=datetime.now(),
            description=response["description"],
            forms_data=response["forms_data"],
            suggestions=response["suggestions"],
            validation=response["validation"],
            applied_to=[]
        )

class SuggestionsState:
    """Gerenciador de estado das sugestões."""
    
    @staticmethod
    def get_buffer() -> Optional[SuggestionBuffer]:
        """Obtém buffer atual."""
        if "suggestions_buffer" not in st.session_state:
            return None
        return st.session_state.suggestions_buffer
    
    @staticmethod
    def set_buffer(buffer: SuggestionBuffer) -> None:
        """Define buffer atual."""
        if not hasattr(st.session_state, 'suggestions_buffer'):
            st.session_state['suggestions_buffer'] = None
        st.session_state['suggestions_buffer'] = buffer
    
    @staticmethod
    def clear_buffer() -> None:
        """Limpa buffer atual."""
        if "suggestions_buffer" in st.session_state:
            st.session_state["suggestions_buffer"] = None
    
    @staticmethod
    def mark_as_applied(form_id: str) -> None:
        """Marca sugestões como aplicadas para um formulário."""
        buffer = SuggestionsState.get_buffer()
        if buffer and buffer.applied_to is not None:
            if form_id not in buffer.applied_to:
                buffer.applied_to.append(form_id)
    
    @staticmethod
    def is_applied(form_id: str) -> bool:
        """Verifica se sugestões foram aplicadas para um formulário."""
        buffer = SuggestionsState.get_buffer()
        return buffer and buffer.applied_to and form_id in buffer.applied_to 