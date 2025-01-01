"""Gerenciador de sugestões da IA."""
import streamlit as st
from typing import List, Dict, Optional
from src.services.ai_service import AIService
from src.services.ai_types import AIResponse, FormData, SuggestionPreview
from src.utils.logger import Logger

class SuggestionsManager:
    """Gerenciador de sugestões da IA."""
    
    def __init__(self, api_key: str):
        """
        Inicializa o gerenciador.
        
        Args:
            api_key: Chave da API OpenAI
        """
        self.ai_service = AIService(api_key)
        self.logger = Logger()
        
        # Inicializa estado
        if "suggestions_buffer" not in st.session_state:
            st.session_state.suggestions_buffer = None
    
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
            with st.spinner("Gerando sugestões..."):
                suggestions = await self.ai_service.suggest_improvements(
                    description,
                    current_data
                )
                st.session_state.suggestions_buffer = suggestions
                
        except Exception as e:
            self.logger.error(f"Erro ao solicitar sugestões: {str(e)}")
            st.error("Não foi possível gerar sugestões. Tente novamente.")
    
    def render_preview(self) -> None:
        """Renderiza preview das sugestões."""
        if not st.session_state.suggestions_buffer:
            return
            
        suggestions = st.session_state.suggestions_buffer
        
        st.write("### 📝 Sugestões de Melhoria")
        
        # Descrição melhorada
        with st.expander("✨ Descrição Formal", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Original:**")
                st.text(suggestions["description"])
            with col2:
                st.write("**Sugerido:**")
                st.text(suggestions["description"])
            
            if st.button("Aplicar Melhoria"):
                self._apply_description(suggestions["description"])
        
        # Sugestões gerais
        if suggestions["suggestions"]:
            with st.expander("💡 Sugestões", expanded=True):
                for suggestion in suggestions["suggestions"]:
                    st.info(suggestion)
        
        # Validações
        if suggestions["validation"]:
            with st.expander("⚠️ Validações", expanded=True):
                for validation in suggestions["validation"]:
                    st.warning(validation)
        
        # Formulários
        if suggestions["forms_data"]:
            with st.expander("📋 Dados Sugeridos", expanded=True):
                selected_forms = []
                
                for form_id, form_data in suggestions["forms_data"].items():
                    st.write(f"**{form_id.title()}**")
                    
                    # Mostra dados sugeridos
                    st.json(form_data["data"])
                    
                    # Checkbox para seleção
                    if st.checkbox(f"Aplicar em {form_id}", key=f"apply_{form_id}"):
                        selected_forms.append(form_id)
                
                # Botões de ação
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Aplicar Selecionados", disabled=not selected_forms):
                        self._apply_suggestions(selected_forms)
                        st.success("Sugestões aplicadas com sucesso!")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Descartar"):
                        self._discard_suggestions()
                        st.rerun()
    
    def _apply_description(self, description: str) -> None:
        """
        Aplica descrição melhorada.
        
        Args:
            description: Nova descrição
        """
        if "process_data" not in st.session_state:
            st.session_state.process_data = {}
            
        st.session_state.process_data["description"] = description
    
    def _apply_suggestions(self, selected_forms: List[str]) -> None:
        """
        Aplica sugestões aos formulários selecionados.
        
        Args:
            selected_forms: Lista de IDs dos formulários
        """
        if not st.session_state.suggestions_buffer:
            return
            
        suggestions = st.session_state.suggestions_buffer
        
        for form_id in selected_forms:
            if form_id in suggestions["forms_data"]:
                form_data = suggestions["forms_data"][form_id]
                
                # Atualiza dados do formulário
                if form_id not in st.session_state:
                    st.session_state[form_id] = {}
                    
                st.session_state[form_id].update(form_data["data"])
    
    def _discard_suggestions(self) -> None:
        """Descarta sugestões atuais."""
        st.session_state.suggestions_buffer = None 