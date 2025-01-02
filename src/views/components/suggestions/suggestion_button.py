"""Componente de botão de sugestões."""
import streamlit as st
from typing import Optional, Dict
from src.views.components.suggestions.suggestions_manager import SuggestionsManager

class SuggestionButton:
    """Botão de sugestões com preview."""
    
    def __init__(self):
        """Inicializa o componente."""
        self.manager = SuggestionsManager()
    
    async def render(
        self,
        description: str,
        current_data: Optional[Dict] = None,
        disabled: bool = False
    ) -> None:
        """
        Renderiza o botão de sugestões.
        
        Args:
            description: Descrição do processo
            current_data: Dados atuais do formulário
            disabled: Se o botão deve estar desabilitado
        """
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button(
                "🤖 Gerar Sugestões",
                disabled=disabled,
                use_container_width=True,
                key="btn_suggestions"
            ):
                st.session_state.requesting_suggestions = True
        
        with col2:
            if disabled:
                st.info("Preencha a descrição para gerar sugestões")
        
        # Processa sugestões se solicitado
        if getattr(st.session_state, 'requesting_suggestions', False):
            with st.spinner("Gerando sugestões..."):
                await self.manager.request_suggestions(description, current_data)
            st.session_state.requesting_suggestions = False
            st.rerun()
        
        # Renderiza preview se houver sugestões
        if st.session_state.suggestions_buffer:
            self.manager.render_preview() 