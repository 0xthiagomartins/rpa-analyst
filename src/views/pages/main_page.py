"""Página principal da aplicação."""
import streamlit as st
from typing import Optional
import asyncio
from utils.dependency_container import DependencyContainer
from views.components import (
    get_process_timeline,
    get_validation_summary,
    get_navigation_bar
)
from views.components.forms.identification_form import IdentificationForm

class MainPage:
    """Página principal da aplicação."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa a página."""
        self.container = container or DependencyContainer()
        self.timeline = get_process_timeline()(container)
        self.validation = get_validation_summary()(container)
        self.navbar = get_navigation_bar()(container)
        self._setup_forms()

    def _setup_forms(self):
        """Configura os formulários."""
        self.forms = {
            "identification": IdentificationForm()
            # ... outros formulários
        }
    
    async def _render_current_form(self):
        """Renderiza o formulário atual."""
        current_form = st.session_state.get("current_form", "identification")
        form = self.forms.get(current_form)
        if form:
            await form.render()
        else:
            st.error("Formulário não encontrado")

    def render(self):
        """Renderiza a página."""
        # Cabeçalho
        st.markdown('<h1 class="main-header">🤖 Agente Analista de RPA</h1>', unsafe_allow_html=True)
        
        # Timeline do processo
        col1, col2 = st.columns([2, 1])
        with col1:
            self.timeline.render()
        
        # Área principal de conteúdo
        st.markdown('<div class="section-header">📝 Formulário</div>', unsafe_allow_html=True)
        
        # Tabs de navegação
        self.navbar.render(style="tabs")
        
        # Área do formulário atual
        with st.container():
            # Executa o formulário assíncrono
            asyncio.run(self._render_current_form()) 