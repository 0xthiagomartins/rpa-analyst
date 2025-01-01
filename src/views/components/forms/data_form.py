"""Formulário de dados do processo."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.forms.form_base import BaseForm
from views.components.forms.form_field import FormField

class DataForm(BaseForm):
    """Formulário para dados do processo."""
    
    DATA_TYPES = [
        "Texto", "Número", "Data", "Booleano", "Lista", 
        "Documento", "Imagem", "Planilha", "JSON", "XML", "Outro"
    ]
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("data", container)
        
        # Inicializa campos
        self.inputs_field = FormField(self.form_id, "inputs")
        self.outputs_field = FormField(self.form_id, "outputs")
        self.validations_field = FormField(self.form_id, "validations")
        
        # Inicializa listas se não existirem
        if "inputs_list" not in st.session_state:
            st.session_state.inputs_list = self.form_data.data.get("inputs", [])
        if "outputs_list" not in st.session_state:
            st.session_state.outputs_list = self.form_data.data.get("outputs", [])
        if "validations_list" not in st.session_state:
            st.session_state.validations_list = self.form_data.data.get("validations", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida dados de entrada
        if not st.session_state.inputs_list:
            errors.append("Pelo menos um dado de entrada é obrigatório")
            is_valid = False
        
        # Valida dados de saída
        if not st.session_state.outputs_list:
            errors.append("Pelo menos um dado de saída é obrigatório")
            is_valid = False
        
        # Valida tipos de dados
        for input_data in st.session_state.inputs_list:
            if not input_data.get("type") or not input_data.get("description"):
                errors.append(f"O dado '{input_data.get('name')}' precisa ter tipo e descrição")
                is_valid = False
        
        for output_data in st.session_state.outputs_list:
            if not output_data.get("type") or not output_data.get("description"):
                errors.append(f"O dado '{output_data.get('name')}' precisa ter tipo e descrição")
                is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_data_field(self, field_type: str) -> None:
        """
        Adiciona um novo campo de dado.
        
        Args:
            field_type: Tipo do campo (input/output)
        """
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Nome do {field_type}", key=f"new_{field_type}_name")
        with col2:
            data_type = st.selectbox(
                "Tipo de Dado",
                options=self.DATA_TYPES,
                key=f"new_{field_type}_type"
            )
            
        description = st.text_area(
            "Descrição",
            key=f"new_{field_type}_desc",
            help="Descreva o dado e seu propósito"
        )
            
        if st.button(f"➕ Adicionar {field_type.title()}"):
            if name and data_type and description:
                new_data = {
                    "name": name,
                    "type": data_type,
                    "description": description
                }
                
                if field_type == "input":
                    st.session_state.inputs_list.append(new_data)
                    self.update_field("inputs", st.session_state.inputs_list)
                else:
                    st.session_state.outputs_list.append(new_data)
                    self.update_field("outputs", st.session_state.outputs_list)
                    
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_validation(self) -> None:
        """Adiciona uma nova regra de validação."""
        data_field = st.text_input("Campo de Dado", key="new_validation_field")
        rule = st.text_area(
            "Regra de Validação",
            key="new_validation_rule",
            help="Ex: Não pode estar vazio, Deve ser maior que zero, etc."
        )
            
        if st.button("➕ Adicionar Validação"):
            if data_field and rule:
                new_validation = {
                    "field": data_field,
                    "rule": rule
                }
                st.session_state.validations_list.append(new_validation)
                self.update_field("validations", st.session_state.validations_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("📊 Dados do Processo")
        
        # Seção de Dados de Entrada
        st.write("#### Dados de Entrada")
        
        # Lista dados de entrada existentes
        for i, input_data in enumerate(st.session_state.inputs_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_name = st.text_input(
                    "Nome",
                    value=input_data["name"],
                    key=f"input_name_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_type = st.selectbox(
                    "Tipo",
                    options=self.DATA_TYPES,
                    index=self.DATA_TYPES.index(input_data["type"]),
                    key=f"input_type_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_input_{i}"):
                    st.session_state.inputs_list.pop(i)
                    self.update_field("inputs", st.session_state.inputs_list)
                    st.rerun()
            
            new_description = st.text_area(
                "Descrição",
                value=input_data["description"],
                key=f"input_desc_{i}",
                disabled=not self.is_editing
            )
            
            if self.is_editing and (
                new_name != input_data["name"] or 
                new_type != input_data["type"] or
                new_description != input_data["description"]
            ):
                st.session_state.inputs_list[i] = {
                    "name": new_name,
                    "type": new_type,
                    "description": new_description
                }
                self.update_field("inputs", st.session_state.inputs_list)
        
        # Adicionar novo dado de entrada
        if self.is_editing:
            self._add_data_field("input")
        
        # Seção de Dados de Saída
        st.write("#### Dados de Saída")
        
        # Lista dados de saída existentes
        for i, output_data in enumerate(st.session_state.outputs_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_name = st.text_input(
                    "Nome",
                    value=output_data["name"],
                    key=f"output_name_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_type = st.selectbox(
                    "Tipo",
                    options=self.DATA_TYPES,
                    index=self.DATA_TYPES.index(output_data["type"]),
                    key=f"output_type_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_output_{i}"):
                    st.session_state.outputs_list.pop(i)
                    self.update_field("outputs", st.session_state.outputs_list)
                    st.rerun()
            
            new_description = st.text_area(
                "Descrição",
                value=output_data["description"],
                key=f"output_desc_{i}",
                disabled=not self.is_editing
            )
            
            if self.is_editing and (
                new_name != output_data["name"] or 
                new_type != output_data["type"] or
                new_description != output_data["description"]
            ):
                st.session_state.outputs_list[i] = {
                    "name": new_name,
                    "type": new_type,
                    "description": new_description
                }
                self.update_field("outputs", st.session_state.outputs_list)
        
        # Adicionar novo dado de saída
        if self.is_editing:
            self._add_data_field("output")
        
        # Seção de Validações
        st.write("#### Regras de Validação")
        
        # Lista validações existentes
        for i, validation in enumerate(st.session_state.validations_list):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_field = st.text_input(
                    "Campo",
                    value=validation["field"],
                    key=f"validation_field_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_rule = st.text_input(
                    "Regra",
                    value=validation["rule"],
                    key=f"validation_rule_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_validation_{i}"):
                    st.session_state.validations_list.pop(i)
                    self.update_field("validations", st.session_state.validations_list)
                    st.rerun()
            
            if self.is_editing and (
                new_field != validation["field"] or 
                new_rule != validation["rule"]
            ):
                st.session_state.validations_list[i] = {
                    "field": new_field,
                    "rule": new_rule
                }
                self.update_field("validations", st.session_state.validations_list)
        
        # Adicionar nova validação
        if self.is_editing:
            self._add_validation() 