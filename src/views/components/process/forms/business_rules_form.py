"""Módulo do formulário de regras de negócio."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class BusinessRulesForm(FormBase):
    """Formulário para regras de negócio e exceções do processo."""
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "business_rules")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_rule(self, rules: List[str]) -> None:
        """Adiciona uma nova regra à lista."""
        new_rule = st.text_area(
            "Nova Regra",
            key="new_rule",
            help="Descreva uma regra de negócio"
        )
        if st.button("➕ Adicionar Regra") and new_rule:
            rules.append(new_rule)
    
    def _add_exception(self, exceptions: List[str]) -> None:
        """Adiciona uma nova exceção à lista."""
        new_exception = st.text_area(
            "Nova Exceção",
            key="new_exception",
            help="Descreva uma exceção do processo"
        )
        if st.button("➕ Adicionar Exceção") and new_exception:
            exceptions.append(new_exception)
        
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📜 Regras de Negócio e Exceções")
        
        # Inicializa listas se não existirem
        if "business_rules" not in self._data:
            self._data["business_rules"] = []
        if "exceptions" not in self._data:
            self._data["exceptions"] = []
            
        # Seção de Regras de Negócio
        st.write("#### Regras de Negócio")
        rules = self._data["business_rules"]
        
        # Lista regras existentes
        for i, rule in enumerate(rules):
            col1, col2 = st.columns([4, 1])
            with col1:
                rules[i] = st.text_area(f"Regra {i+1}", value=rule, key=f"rule_{i}")
            with col2:
                if st.button("🗑️", key=f"del_rule_{i}"):
                    rules.pop(i)
                    st.rerun()
        
        # Adicionar nova regra
        self._add_rule(rules)
        
        # Seção de Exceções
        st.write("#### Exceções")
        exceptions = self._data["exceptions"]
        
        # Lista exceções existentes
        for i, exception in enumerate(exceptions):
            col1, col2 = st.columns([4, 1])
            with col1:
                exceptions[i] = st.text_area(f"Exceção {i+1}", value=exception, key=f"exception_{i}")
            with col2:
                if st.button("🗑️", key=f"del_exception_{i}"):
                    exceptions.pop(i)
                    st.rerun()
        
        # Adicionar nova exceção
        self._add_exception(exceptions) 