"""Formulário de identificação do processo."""
import streamlit as st
from typing import Optional, Dict
from src.views.components.suggestions.suggestion_button import SuggestionButton

class IdentificationForm:
    """Formulário de identificação do processo."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o formulário.
        
        Args:
            api_key: Chave da API OpenAI (opcional)
        """
        self.suggestion_button = (
            SuggestionButton(api_key) if api_key else None
        )
    
    async def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### Identificação do Processo")
        
        # Campos do formulário
        description = st.text_area(
            "Descrição do Processo",
            value=st.session_state.get('process_data', {}).get('description', ''),
            help="Descreva o processo em detalhes"
        )
        
        name = st.text_input(
            "Nome do Processo",
            value=st.session_state.get('process_data', {}).get('name', ''),
            help="Nome curto e descritivo"
        )
        
        responsible = st.text_input(
            "Responsável",
            value=st.session_state.get('process_data', {}).get('responsible', ''),
            help="Pessoa/equipe responsável"
        )
        
        area = st.text_input(
            "Área",
            value=st.session_state.get('process_data', {}).get('area', ''),
            help="Área/departamento do processo"
        )
        
        # Atualiza dados na sessão
        if 'process_data' not in st.session_state:
            st.session_state.process_data = {}
            
        st.session_state.process_data.update({
            'description': description,
            'name': name,
            'responsible': responsible,
            'area': area
        })
        
        # Botão de sugestões (se configurado)
        if self.suggestion_button and description:
            st.write("---")
            await self.suggestion_button.render(
                description=description,
                current_data=st.session_state.get('process_data'),
                disabled=not description
            ) 