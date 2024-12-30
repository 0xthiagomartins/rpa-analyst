"""Módulo do formulário de identificação."""
from typing import Dict, Any
import streamlit as st
from .form_base import FormBase

class IdentificationForm(FormBase):
    """Formulário para identificação do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "identification")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 🎯 Identificação do Processo")
        
        self._data["process_name"] = st.text_input(
            "Nome do Processo",
            value=self._data.get("process_name", ""),
            help="Nome do processo a ser automatizado"
        )
        
        self._data["process_owner"] = st.text_input(
            "Responsável pelo Processo",
            value=self._data.get("process_owner", ""),
            help="Nome do responsável pelo processo"
        )
        
        self._data["department"] = st.text_input(
            "Departamento",
            value=self._data.get("department", ""),
            help="Departamento responsável pelo processo"
        )
        
        self._data["current_status"] = st.selectbox(
            "Status Atual",
            options=["Em andamento", "Concluído", "Pendente"],
            index=0 if "current_status" not in self._data else ["Em andamento", "Concluído", "Pendente"].index(self._data["current_status"])
        )
        
        self._data["estimated_time"] = st.text_input(
            "Tempo Estimado",
            value=self._data.get("estimated_time", ""),
            help="Tempo estimado para conclusão do processo"
        ) 