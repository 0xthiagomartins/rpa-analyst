"""Formulário de identificação do processo."""
import streamlit as st
from typing import Optional, Dict
from src.utils.logger import Logger
from ..form_base import SuggestibleForm
from src.views.suggestions.suggestions_manager import SuggestionsManager

class IdentificationForm(SuggestibleForm):
    """Formulário de identificação do processo."""
    
    def __init__(self):
        """Inicializa o formulário."""
        super().__init__()
        self.suggestions_manager = SuggestionsManager()
        self.logger = Logger()
        self._process_description = ""

    @property
    def process_description(self) -> str:
        """Retorna a descrição do processo."""
        return st.session_state.get("process_description", "")

    async def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📋 Identificação do Processo")
        
        # Campos do formulário
        process_name = st.text_input(
            "Nome do Processo",
            value=st.session_state.get("process_name", ""),
            help="Nome que identifica o processo"
        )
        
        process_owner = st.text_input(
            "Responsável",
            value=st.session_state.get("process_owner", ""),
            help="Pessoa responsável pelo processo"
        )
        
        process_description = st.text_area(
            "Descrição",
            value=st.session_state.get("process_description", ""),
            help="Descrição detalhada do processo"
        )
        
        # Atualiza session_state
        st.session_state.update({
            'process_name': process_name,
            'process_owner': process_owner,
            'process_description': process_description
        })
        
        # Renderiza sugestões se disponíveis
        await self.render_suggestions()

    async def render_suggestions(self) -> None:
        """Renderiza sugestões se disponíveis."""
        if self.process_description:
            st.write("---")
            try:
                # Botão de gerar sugestões
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(
                        "🤖 Gerar Sugestões",
                        use_container_width=True,
                        key="btn_suggestions"
                    ):
                        st.session_state.requesting_suggestions = True
                
                # Processa sugestões se solicitado
                if getattr(st.session_state, 'requesting_suggestions', False):
                    with st.spinner("Gerando sugestões..."):
                        await self.suggestions_manager.request_suggestions(
                            description=self.process_description,
                            current_data=st.session_state.get('process_data')
                        )
                    st.session_state.requesting_suggestions = False
                    st.rerun()
                
                # Renderiza preview de sugestões
                await self.suggestions_manager.render_preview()
                
            except Exception as e:
                self.logger.error(f"Erro ao processar sugestões: {str(e)}")
                st.error("Não foi possível gerar sugestões. Tente novamente.") 