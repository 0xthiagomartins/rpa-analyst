"""Módulo do formulário de detalhes do processo."""
from typing import Dict, Any
import streamlit as st
from .form_base import FormBase

class ProcessDetailsForm(FormBase):
    """Formulário para detalhes do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
        
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "process_details")
        return len(errors) == 0
        
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📋 Detalhes do Processo")
        
        self._data["steps_as_is"] = st.text_area(
            "Passos do Processo (As-Is)",
            value=self._data.get("steps_as_is", ""),
            help="Descreva os passos atuais do processo"
        )
        
        self._data["systems"] = st.text_area(
            "Sistemas/Ferramentas",
            value=self._data.get("systems", ""),
            help="Liste os sistemas e ferramentas utilizados"
        )
        
        self._data["data_used"] = st.text_area(
            "Dados Utilizados",
            value=self._data.get("data_used", ""),
            help="Descreva os dados manipulados no processo"
        ) 