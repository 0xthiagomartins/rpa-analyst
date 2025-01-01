"""Formulário de detalhes do processo."""
from typing import Optional
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.forms.form_base import BaseForm
from views.components.forms.form_field import FormField

class ProcessDetailsForm(BaseForm):
    """Formulário para detalhes do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("details", container)
        
        # Inicializa campos
        self.steps_field = FormField(self.form_id, "steps_as_is")
        self.systems_field = FormField(self.form_id, "systems")
        self.data_field = FormField(self.form_id, "data_used")
        self.volume_field = FormField(self.form_id, "volume")
        self.frequency_field = FormField(self.form_id, "frequency")
        self.additional_info_field = FormField(self.form_id, "additional_info")
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida passos do processo
        if not self.form_data.data.get("steps_as_is"):
            errors.append("Passos do processo são obrigatórios")
            is_valid = False
        
        # Valida sistemas/ferramentas
        if not self.form_data.data.get("systems"):
            errors.append("Sistemas/ferramentas são obrigatórios")
            is_valid = False
        
        # Valida dados utilizados
        if not self.form_data.data.get("data_used"):
            errors.append("Dados utilizados são obrigatórios")
            is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("📋 Detalhes do Processo")
        
        # Passos do processo
        new_steps = self.steps_field.render_text_area(
            "Passos do Processo (As-Is)",
            value=self.form_data.data.get("steps_as_is", ""),
            is_disabled=not self.is_editing,
            help="Descreva os passos atuais do processo",
            height=150
        )
        if self.is_editing:
            self.update_field("steps_as_is", new_steps)
        
        # Sistemas e dados em duas colunas
        col1, col2 = st.columns(2)
        
        with col1:
            new_systems = self.systems_field.render_text_area(
                "Sistemas/Ferramentas",
                value=self.form_data.data.get("systems", ""),
                is_disabled=not self.is_editing,
                help="Liste os sistemas e ferramentas utilizados",
                height=100
            )
            if self.is_editing:
                self.update_field("systems", new_systems)
        
        with col2:
            new_data = self.data_field.render_text_area(
                "Dados Utilizados",
                value=self.form_data.data.get("data_used", ""),
                is_disabled=not self.is_editing,
                help="Descreva os dados manipulados no processo",
                height=100
            )
            if self.is_editing:
                self.update_field("data_used", new_data)
        
        # Volume e frequência em duas colunas
        col1, col2 = st.columns(2)
        
        with col1:
            new_volume = self.volume_field.render_text_input(
                "Volume de Processamento",
                value=self.form_data.data.get("volume", ""),
                is_disabled=not self.is_editing,
                help="Volume médio de processamento (ex: 100 registros/dia)"
            )
            if self.is_editing:
                self.update_field("volume", new_volume)
        
        with col2:
            new_frequency = self.frequency_field.render_text_input(
                "Frequência",
                value=self.form_data.data.get("frequency", ""),
                is_disabled=not self.is_editing,
                help="Frequência de execução (ex: diário, semanal)"
            )
            if self.is_editing:
                self.update_field("frequency", new_frequency)
        
        # Informações adicionais
        new_info = self.additional_info_field.render_text_area(
            "Informações Adicionais",
            value=self.form_data.data.get("additional_info", ""),
            is_disabled=not self.is_editing,
            help="Outras informações relevantes",
            height=100
        )
        if self.is_editing:
            self.update_field("additional_info", new_info) 