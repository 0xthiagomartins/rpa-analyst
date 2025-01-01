"""Formulário de identificação do processo."""
from typing import Optional
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.forms.form_base import BaseForm
from views.components.forms.form_field import FormField

class IdentificationForm(BaseForm):
    """Formulário de identificação do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("identification", container)
        
        # Inicializa campos
        self.process_name_field = FormField(self.form_id, "process_name")
        self.owner_field = FormField(self.form_id, "owner")
        self.description_field = FormField(self.form_id, "description")
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida nome do processo
        if not self.form_data.data.get("process_name"):
            errors.append("Nome do processo é obrigatório")
            is_valid = False
        
        # Valida responsável
        if not self.form_data.data.get("owner"):
            errors.append("Responsável é obrigatório")
            is_valid = False
        
        # Valida descrição
        if not self.form_data.data.get("description"):
            errors.append("Descrição é obrigatória")
            is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("🎯 Identificação do Processo")
        
        # Nome e responsável lado a lado
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = self.process_name_field.render_text_input(
                "Nome do Processo",
                value=self.form_data.data.get("process_name", ""),
                is_disabled=not self.is_editing,
                help="Nome do processo a ser automatizado"
            )
            if self.is_editing:
                self.update_field("process_name", new_name)
            
        with col2:
            new_owner = self.owner_field.render_text_input(
                "Responsável",
                value=self.form_data.data.get("owner", ""),
                is_disabled=not self.is_editing,
                help="Nome do responsável pelo processo"
            )
            if self.is_editing:
                self.update_field("owner", new_owner)
        
        # Descrição em baixo
        new_description = self.description_field.render_text_area(
            "Descrição",
            value=self.form_data.data.get("description", ""),
            is_disabled=not self.is_editing,
            help="Breve descrição do processo",
            height=100
        )
        if self.is_editing:
            self.update_field("description", new_description) 