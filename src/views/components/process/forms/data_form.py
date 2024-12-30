"""Módulo do formulário de dados."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class DataForm(FormBase):
    """Formulário para dados e arquivos do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "data")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_input(self, inputs: List[Dict[str, str]]) -> None:
        """Adiciona uma nova entrada de dados."""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Nome do Dado",
                key="new_input_name",
                help="Nome do dado de entrada"
            )
        with col2:
            data_type = st.selectbox(
                "Tipo",
                options=["Texto", "Número", "Data", "Arquivo", "Outro"],
                key="new_input_type"
            )
            
        description = st.text_area(
            "Descrição",
            key="new_input_description",
            help="Descreva o dado e seu formato"
        )
            
        if st.button("➕ Adicionar Entrada") and name:
            inputs.append({
                "name": name,
                "type": data_type,
                "description": description
            })
    
    def _add_output(self, outputs: List[Dict[str, str]]) -> None:
        """Adiciona uma nova saída de dados."""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Nome do Dado",
                key="new_output_name",
                help="Nome do dado de saída"
            )
        with col2:
            data_type = st.selectbox(
                "Tipo",
                options=["Texto", "Número", "Data", "Arquivo", "Outro"],
                key="new_output_type"
            )
            
        description = st.text_area(
            "Descrição",
            key="new_output_description",
            help="Descreva o dado e seu formato"
        )
            
        if st.button("➕ Adicionar Saída") and name:
            outputs.append({
                "name": name,
                "type": data_type,
                "description": description
            })
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📊 Dados do Processo")
        
        # Inicializa listas se não existirem
        if "inputs" not in self._data:
            self._data["inputs"] = []
        if "outputs" not in self._data:
            self._data["outputs"] = []
            
        # Seção de Entradas
        st.write("#### Dados de Entrada")
        inputs = self._data["inputs"]
        
        # Lista entradas existentes
        for i, input_data in enumerate(inputs):
            with st.expander(f"Entrada {i+1}: {input_data['name']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    inputs[i]["name"] = st.text_input(
                        "Nome",
                        value=input_data["name"],
                        key=f"input_name_{i}"
                    )
                    inputs[i]["type"] = st.selectbox(
                        "Tipo",
                        options=["Texto", "Número", "Data", "Arquivo", "Outro"],
                        index=["Texto", "Número", "Data", "Arquivo", "Outro"].index(input_data["type"]),
                        key=f"input_type_{i}"
                    )
                    inputs[i]["description"] = st.text_area(
                        "Descrição",
                        value=input_data["description"],
                        key=f"input_description_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_input_{i}"):
                        inputs.pop(i)
                        st.rerun()
        
        # Adicionar nova entrada
        self._add_input(inputs)
        
        # Seção de Saídas
        st.write("#### Dados de Saída")
        outputs = self._data["outputs"]
        
        # Lista saídas existentes
        for i, output_data in enumerate(outputs):
            with st.expander(f"Saída {i+1}: {output_data['name']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    outputs[i]["name"] = st.text_input(
                        "Nome",
                        value=output_data["name"],
                        key=f"output_name_{i}"
                    )
                    outputs[i]["type"] = st.selectbox(
                        "Tipo",
                        options=["Texto", "Número", "Data", "Arquivo", "Outro"],
                        index=["Texto", "Número", "Data", "Arquivo", "Outro"].index(output_data["type"]),
                        key=f"output_type_{i}"
                    )
                    outputs[i]["description"] = st.text_area(
                        "Descrição",
                        value=output_data["description"],
                        key=f"output_description_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_output_{i}"):
                        outputs.pop(i)
                        st.rerun()
        
        # Adicionar nova saída
        self._add_output(outputs) 