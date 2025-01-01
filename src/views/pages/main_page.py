"""Página principal da aplicação."""
import streamlit as st
from typing import Optional
from utils.dependency_container import DependencyContainer
from views.components import (
    get_process_timeline,
    get_validation_summary,
    get_navigation_bar
)
from views.components.forms.identification_form import IdentificationForm
from views.components.state.state_manager import StateManager
from views.components.forms.process_details_form import ProcessDetailsForm
from views.components.forms.business_rules_form import BusinessRulesForm
from views.components.forms.automation_goals_form import AutomationGoalsForm
from views.components.forms.systems_form import SystemsForm
from views.components.forms.data_form import DataForm
from views.components.forms.steps_form import StepsForm
from views.components.forms.risks_form import RisksForm
from views.components.forms.documentation_form import DocumentationForm
from views.pages.base_page import BasePage

class MainPage(BasePage):
    """Página principal da aplicação."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa a página."""
        super().__init__(container)
        self.state_manager = StateManager()
        
        # Componentes de UI (lazy loading)
        ProcessTimeline = get_process_timeline()
        ValidationSummary = get_validation_summary()
        NavigationBar = get_navigation_bar()
        
        self.timeline = ProcessTimeline(container)
        self.validation = ValidationSummary(container)
        self.navbar = NavigationBar(container)
    
    def _render_current_form(self) -> None:
        """Renderiza o formulário atual."""
        current_form = self.state_manager.get_current_form()
        
        if current_form == "identification":
            form = IdentificationForm(self.container)
            form.render()
        elif current_form == "details":
            form = ProcessDetailsForm(self.container)
            form.render()
        elif current_form == "rules":
            form = BusinessRulesForm(self.container)
            form.render()
        elif current_form == "automation":
            form = AutomationGoalsForm(self.container)
            form.render()
        elif current_form == "systems":
            form = SystemsForm(self.container)
            form.render()
        elif current_form == "data":
            form = DataForm(self.container)
            form.render()
        elif current_form == "steps":
            form = StepsForm(self.container)
            form.render()
        elif current_form == "risks":
            form = RisksForm(self.container)
            form.render()
        elif current_form == "documentation":
            form = DocumentationForm(self.container)
            form.render()
        else:
            st.info("Selecione um formulário para começar")
    
    def render(self) -> None:
        """Renderiza a página."""
        # Sidebar com navegação
        with st.sidebar:
            st.image("https://raw.githubusercontent.com/Nassim-Tecnologia/brand-assets/refs/heads/main/logo-marca-dark-without-bg.png", width=100)
            st.markdown("### 🤖 Agente Analista")
            
            # Botões de navegação
            if st.button("📝 Novo Processo"):
                st.query_params["page"] = "/process/new"
            
            if st.button("📋 Ver Processos"):
                st.query_params["page"] = "/process/view"
            
            self.navbar.render(style="sidebar")
            
            # Resumo de validação na sidebar
            with st.expander("📊 Status", expanded=True):
                self.validation.render()
        
        # Conteúdo principal
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
            self._render_current_form() 