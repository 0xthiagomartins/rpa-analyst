"""Módulo orquestrador dos formulários de processo."""
from typing import Optional, Dict, Any
import streamlit as st
from src.utils.dependency_container import DependencyContainer
from .identification_form import IdentificationForm
from .process_details_form import ProcessDetailsForm
from .business_rules_form import BusinessRulesForm
from .automation_goals_form import AutomationGoalsForm

class ProcessForm:
    """Orquestrador dos formulários do processo."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa o orquestrador."""
        self.container = container or DependencyContainer()
        self.forms = {
            "identification": IdentificationForm(container),
            "details": ProcessDetailsForm(container),
            "rules": BusinessRulesForm(container),
            "goals": AutomationGoalsForm(container)
        }
        self._current_step = 0
        
    def render(self) -> None:
        """Renderiza o formulário atual."""
        steps = ["Identificação", "Detalhes", "Regras", "Objetivos"]
        
        # Progress bar
        progress = st.progress(self._current_step / len(steps))
        st.write(f"Etapa {self._current_step + 1} de {len(steps)}: {steps[self._current_step]}")
        
        # Renderiza formulário atual
        current_form = list(self.forms.values())[self._current_step]
        current_form.render()
        
        # Botões de navegação
        col1, col2 = st.columns(2)
        with col1:
            if self._current_step > 0:
                if st.button("⬅️ Anterior"):
                    self._current_step -= 1
                    
        with col2:
            if self._current_step < len(steps) - 1:
                if st.button("Próximo ➡️"):
                    if current_form.validate():
                        self._current_step += 1
                    else:
                        st.error("Por favor, preencha todos os campos obrigatórios")
            else:
                if st.button("✅ Finalizar"):
                    if self.validate_all():
                        self.save()
                        
    def validate_all(self) -> bool:
        """Valida todos os formulários."""
        return all(form.validate() for form in self.forms.values())
        
    def save(self) -> None:
        """Salva os dados de todos os formulários."""
        data = {}
        for form in self.forms.values():
            data.update(form.data)
            
        if self.container.resolve(ProcessController).create_process(data):
            st.success("Processo salvo com sucesso!")
        else:
            st.error("Erro ao salvar processo") 