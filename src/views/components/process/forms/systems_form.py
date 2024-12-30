"""Módulo do formulário de sistemas."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class SystemsForm(FormBase):
    """Formulário para sistemas e integrações do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "systems")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_system(self, systems: List[Dict[str, str]]) -> None:
        """Adiciona um novo sistema."""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Nome do Sistema",
                key="new_system_name",
                help="Nome do sistema ou ferramenta"
            )
        with col2:
            role = st.text_input(
                "Função",
                key="new_system_role",
                help="Função do sistema no processo"
            )
            
        if st.button("➕ Adicionar Sistema") and name and role:
            systems.append({
                "name": name,
                "role": role
            })
    
    def _add_integration(self, integrations: List[Dict[str, str]]) -> None:
        """Adiciona uma nova integração."""
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_input(
                "Sistema Origem",
                key="new_integration_source",
                help="Sistema de origem dos dados"
            )
        with col2:
            target = st.text_input(
                "Sistema Destino",
                key="new_integration_target",
                help="Sistema de destino dos dados"
            )
            
        description = st.text_area(
            "Descrição da Integração",
            key="new_integration_description",
            help="Descreva como os sistemas se integram"
        )
            
        if st.button("➕ Adicionar Integração") and source and target:
            integrations.append({
                "source": source,
                "target": target,
                "description": description
            })
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 💻 Sistemas e Integrações")
        
        # Inicializa listas se não existirem
        if "systems" not in self._data:
            self._data["systems"] = []
        if "integrations" not in self._data:
            self._data["integrations"] = []
            
        # Seção de Sistemas
        st.write("#### Sistemas")
        systems = self._data["systems"]
        
        # Lista sistemas existentes
        for i, system in enumerate(systems):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                systems[i]["name"] = st.text_input(
                    "Nome",
                    value=system["name"],
                    key=f"system_name_{i}"
                )
            with col2:
                systems[i]["role"] = st.text_input(
                    "Função",
                    value=system["role"],
                    key=f"system_role_{i}"
                )
            with col3:
                if st.button("🗑️", key=f"del_system_{i}"):
                    systems.pop(i)
                    st.rerun()
        
        # Adicionar novo sistema
        self._add_system(systems)
        
        # Seção de Integrações
        st.write("#### Integrações")
        integrations = self._data["integrations"]
        
        # Lista integrações existentes
        for i, integration in enumerate(integrations):
            with st.expander(f"Integração {i+1}: {integration['source']} → {integration['target']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    integrations[i]["source"] = st.text_input(
                        "Sistema Origem",
                        value=integration["source"],
                        key=f"integration_source_{i}"
                    )
                    integrations[i]["target"] = st.text_input(
                        "Sistema Destino",
                        value=integration["target"],
                        key=f"integration_target_{i}"
                    )
                    integrations[i]["description"] = st.text_area(
                        "Descrição",
                        value=integration["description"],
                        key=f"integration_description_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_integration_{i}"):
                        integrations.pop(i)
                        st.rerun()
        
        # Adicionar nova integração
        self._add_integration(integrations) 