"""Módulo para gerenciamento do buffer de sugestões."""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import streamlit as st
from src.utils.logger import Logger

@dataclass
class SuggestionData:
    """Dados de uma sugestão."""
    form_id: str
    data: Dict[str, Any]
    confidence: float
    timestamp: datetime
    applied: bool = False

class SuggestionsBuffer:
    """Gerenciador de buffer de sugestões."""
    
    def __init__(self):
        """Inicializa o buffer."""
        self.logger = Logger()
        if 'suggestions_buffer' not in st.session_state:
            st.session_state.suggestions_buffer = {}
    
    def add_suggestion(
        self, 
        form_id: str, 
        data: Dict[str, Any],
        confidence: float = 0.0
    ) -> None:
        """
        Adiciona uma sugestão ao buffer.
        
        Args:
            form_id: ID do formulário
            data: Dados sugeridos
            confidence: Nível de confiança da sugestão
        """
        suggestion = SuggestionData(
            form_id=form_id,
            data=data,
            confidence=confidence,
            timestamp=datetime.now()
        )
        st.session_state.suggestions_buffer[form_id] = suggestion
        self.logger.info(f"Sugestão adicionada para {form_id}")
    
    def get_suggestion(self, form_id: str) -> Optional[SuggestionData]:
        """Retorna sugestão para um formulário."""
        return st.session_state.suggestions_buffer.get(form_id)
    
    def mark_as_applied(self, form_id: str) -> None:
        """Marca sugestão como aplicada."""
        if suggestion := self.get_suggestion(form_id):
            suggestion.applied = True
            self.logger.info(f"Sugestão marcada como aplicada para {form_id}")
    
    def clear_suggestions(self) -> None:
        """Limpa todas as sugestões."""
        st.session_state.suggestions_buffer = {}
        self.logger.info("Buffer de sugestões limpo")
    
    def has_suggestions(self, form_id: str) -> bool:
        """Verifica se há sugestões para um formulário."""
        return form_id in st.session_state.suggestions_buffer 