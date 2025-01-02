"""Formulário de identificação do processo."""
import streamlit as st
from typing import Optional, Dict
from src.utils.logger import Logger
from .form_base import SuggestibleForm

class IdentificationForm(SuggestibleForm):
    """Formulário de identificação do processo."""
    
    def __init__(self):
        """Inicializa o formulário."""
        super().__init__("identification")
        self.logger = Logger()

    async def render(self):
        """Renderiza o formulário."""
        st.write("### 🎯 Identificação do Processo")
        
        # Campos do formulário
        name = st.text_input(
            "Nome do Processo",
            value=st.session_state.get("process_name", ""),
            help="Nome do processo a ser automatizado"
        )
        
        responsible = st.text_input(
            "Responsável",
            value=st.session_state.get("responsible", ""),
            help="Responsável pelo processo"
        )
        
        area = st.text_input(
            "Área",
            value=st.session_state.get("area", ""),
            help="Área/departamento do processo"
        )
        
        description = st.text_area(
            "Descrição do Processo",
            value=st.session_state.get("description", ""),
            help="Descreva o processo em detalhes"
        )
        
        # Atualiza session_state
        st.session_state.update({
            'process_name': name,
            'responsible': responsible,
            'area': area,
            'description': description
        })
        
        # Botão de sugestões e preview
        if description:
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
                            description=description,
                            current_data=st.session_state.get('process_data')
                        )
                    st.session_state.requesting_suggestions = False
                    st.rerun()
                
                # Renderiza preview de sugestões
                self.render_suggestions()
                
            except Exception as e:
                self.logger.error(f"Erro ao processar sugestões: {str(e)}")
                st.error("Não foi possível gerar sugestões. Tente novamente.") 