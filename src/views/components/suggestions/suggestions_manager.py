"""Gerenciador de sugestões da IA."""
import streamlit as st
from typing import List, Dict, Optional
from src.services.ai_service import AIService
from src.services.ai_types import AIResponse, FormData
from src.utils.logger import Logger
from src.views.components.state.suggestions_buffer import SuggestionsState, SuggestionBuffer

class SuggestionsManager:
    """Gerenciador de sugestões da IA."""
    
    def __init__(self):
        """Inicializa o gerenciador."""
        self.logger = Logger()
        self.ai_service = AIService()

    async def request_suggestions(
        self,
        description: str,
        current_data: Optional[Dict] = None
    ) -> None:
        """
        Solicita sugestões da IA.
        
        Args:
            description: Descrição do processo
            current_data: Dados atuais dos formulários
        """
        try:
            # Obtém sugestões da IA
            response = await self.ai_service.analyze_process(
                description=description,
                current_data=current_data or {}
            )
            
            # Armazena no buffer
            buffer = SuggestionBuffer.from_response(response)
            SuggestionsState.set_buffer(buffer)
            
        except Exception as e:
            self.logger.error(f"Erro ao solicitar sugestões: {str(e)}")
            st.error("Não foi possível gerar sugestões. Tente novamente.")

    def render_preview(self, form_id: Optional[str] = None) -> None:
        """
        Renderiza preview das sugestões.
        
        Args:
            form_id: ID do formulário atual (opcional)
        """
        buffer = SuggestionsState.get_buffer()
        if not buffer:
            return
            
        with st.expander("✨ Sugestões da IA", expanded=True):
            # Mostra sugestões gerais
            if buffer.suggestions:
                st.write("##### Sugestões Gerais")
                for suggestion in buffer.suggestions:
                    st.info(suggestion)
            
            # Mostra preview dos formulários
            if buffer.forms_data:
                st.write("##### Sugestões para Formulários")
                
                # Se form_id fornecido, mostra apenas sugestões relevantes
                forms = (
                    [form_id] if form_id and form_id in buffer.forms_data
                    else list(buffer.forms_data.keys())
                )
                
                selected_forms = st.multiselect(
                    "Selecione os formulários para aplicar sugestões:",
                    options=forms,
                    default=forms[0] if forms else None
                )
                
                if selected_forms:
                    if st.button("✅ Aplicar Sugestões Selecionadas"):
                        self._apply_suggestions(selected_forms)
                        st.success("Sugestões aplicadas!")
                        st.rerun()
                    
                    if st.button("❌ Descartar Sugestões"):
                        self._discard_suggestions()
                        st.rerun()

    def _apply_suggestions(self, selected_forms: List[str]) -> None:
        """Aplica sugestões aos formulários selecionados."""
        buffer = SuggestionsState.get_buffer()
        if not buffer:
            return
            
        for form_id in selected_forms:
            if form_id in buffer.forms_data:
                form_data = buffer.forms_data[form_id]["data"]
                
                # Atualiza dados do formulário
                for key, value in form_data.items():
                    if isinstance(value, list):
                        # Para listas, substitui diretamente
                        st.session_state[key] = value.copy()
                    else:
                        # Para outros tipos, usa update se possível
                        if key not in st.session_state:
                            st.session_state[key] = value
                        elif hasattr(st.session_state[key], 'update'):
                            st.session_state[key].update(value)
                        else:
                            st.session_state[key] = value
                
                SuggestionsState.mark_as_applied(form_id)
    
    def _discard_suggestions(self) -> None:
        """Descarta sugestões atuais."""
        SuggestionsState.clear_buffer() 