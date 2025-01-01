"""Formulário de regras de negócio."""
from typing import Optional, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.forms.form_base import BaseForm
from views.components.forms.form_field import FormField

class BusinessRulesForm(BaseForm):
    """Formulário para regras de negócio."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("rules", container)
        
        # Inicializa campos
        self.rules_field = FormField(self.form_id, "business_rules")
        self.exceptions_field = FormField(self.form_id, "exceptions")
        
        # Inicializa listas se não existirem
        if "rules_list" not in st.session_state:
            st.session_state.rules_list = self.form_data.data.get("business_rules", [])
        if "exceptions_list" not in st.session_state:
            st.session_state.exceptions_list = self.form_data.data.get("exceptions", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida regras de negócio
        if not st.session_state.rules_list:
            errors.append("Pelo menos uma regra de negócio é obrigatória")
            is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_rule(self) -> None:
        """Adiciona uma nova regra."""
        new_rule = st.text_area("Nova Regra", key="new_rule")
        if st.button("➕ Adicionar Regra"):
            if new_rule:
                st.session_state.rules_list.append(new_rule)
                self.update_field("business_rules", st.session_state.rules_list)
                st.rerun()
    
    def _add_exception(self) -> None:
        """Adiciona uma nova exceção."""
        new_exception = st.text_area("Nova Exceção", key="new_exception")
        if st.button("➕ Adicionar Exceção"):
            if new_exception:
                st.session_state.exceptions_list.append(new_exception)
                self.update_field("exceptions", st.session_state.exceptions_list)
                st.rerun()
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("📜 Regras de Negócio")
        
        # Seção de Regras
        st.write("#### Regras de Negócio")
        
        # Lista regras existentes
        for i, rule in enumerate(st.session_state.rules_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_rule = st.text_area(
                    f"Regra {i+1}",
                    value=rule,
                    key=f"rule_{i}",
                    disabled=not self.is_editing
                )
                if self.is_editing and new_rule != rule:
                    st.session_state.rules_list[i] = new_rule
                    self.update_field("business_rules", st.session_state.rules_list)
            
            with col2:
                if self.is_editing and st.button("🗑️", key=f"del_rule_{i}"):
                    st.session_state.rules_list.pop(i)
                    self.update_field("business_rules", st.session_state.rules_list)
                    st.rerun()
        
        # Adicionar nova regra
        if self.is_editing:
            self._add_rule()
        
        # Seção de Exceções
        st.write("#### Exceções")
        
        # Lista exceções existentes
        for i, exception in enumerate(st.session_state.exceptions_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_exception = st.text_area(
                    f"Exceção {i+1}",
                    value=exception,
                    key=f"exception_{i}",
                    disabled=not self.is_editing
                )
                if self.is_editing and new_exception != exception:
                    st.session_state.exceptions_list[i] = new_exception
                    self.update_field("exceptions", st.session_state.exceptions_list)
            
            with col2:
                if self.is_editing and st.button("🗑️", key=f"del_exception_{i}"):
                    st.session_state.exceptions_list.pop(i)
                    self.update_field("exceptions", st.session_state.exceptions_list)
                    st.rerun()
        
        # Adicionar nova exceção
        if self.is_editing:
            self._add_exception() 