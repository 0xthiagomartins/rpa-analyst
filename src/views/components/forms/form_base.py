"""Classe base para formulários."""
from typing import Optional, Dict, Any
import json
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState
from views.components.forms.form_field import FormField

class BaseForm:
    """Classe base para formulários com controle de edição."""
    
    def __init__(self, form_id: str, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário base."""
        self.form_id = form_id
        self.container = container
        self.state_manager = StateManager()
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Estado de edição do formulário
        if f"{self.form_id}_edit_mode" not in st.session_state:
            st.session_state[f"{self.form_id}_edit_mode"] = self._is_form_empty()
        
        # Buffer para dados em edição
        if f"{self.form_id}_buffer" not in st.session_state:
            st.session_state[f"{self.form_id}_buffer"] = {}
            
        # Flag para controle de validação
        if f"{self.form_id}_show_validation" not in st.session_state:
            st.session_state[f"{self.form_id}_show_validation"] = False
            
        # Flag para mostrar debug
        if f"{self.form_id}_show_debug" not in st.session_state:
            st.session_state[f"{self.form_id}_show_debug"] = False
    
    def _is_form_empty(self) -> bool:
        """Verifica se o formulário está vazio."""
        return not any(
            value for value in self.form_data.data.values()
            if value and str(value).strip()
        )
    
    @property
    def is_editing(self) -> bool:
        """Retorna se o formulário está em modo de edição."""
        return st.session_state[f"{self.form_id}_edit_mode"]
    
    def update_field(self, field: str, value: Any) -> None:
        """Atualiza um campo no buffer de edição."""
        if self.is_editing:
            st.session_state[f"{self.form_id}_buffer"][field] = value
    
    def _commit_changes(self) -> None:
        """Aplica as mudanças do buffer aos dados do formulário."""
        if self.is_editing:
            buffer = st.session_state[f"{self.form_id}_buffer"]
            self.form_data.data.update(buffer)
            st.session_state[f"{self.form_id}_buffer"] = {}
    
    def _render_debug_section(self) -> None:
        """Renderiza seção de debug com dados do formulário."""
        with st.expander("🔍 Debug"):
            # Dados do formulário
            st.json({
                "form_id": self.form_id,
                "is_editing": self.is_editing,
                "is_empty": self._is_form_empty(),
                "show_validation": st.session_state[f"{self.form_id}_show_validation"],
                "data": self.form_data.data,
                "buffer": st.session_state[f"{self.form_id}_buffer"]
            })
    
    def save(self) -> bool:
        """Salva os dados do formulário."""
        # Aplica mudanças do buffer antes de validar
        self._commit_changes()
        
        # Ativa a validação
        st.session_state[f"{self.form_id}_show_validation"] = True
        
        if not self.validate():
            return False
        
        try:
            self.state_manager.update_form_data(
                self.form_id,
                self.form_data.data,
                is_valid=True
            )
            # Desativa a validação após salvar com sucesso
            st.session_state[f"{self.form_id}_show_validation"] = False
            return True
            
        except Exception as e:
            st.error(f"Erro ao salvar: {str(e)}")
            return False
    
    def render_form_header(self, title: str) -> None:
        """Renderiza o cabeçalho do formulário."""
        st.write(f"### {title}")
        
        col_button = st.columns([3, 1])[1]
        with col_button:
            if not self.is_editing:
                if st.button("✏️ Editar", use_container_width=True):
                    st.session_state[f"{self.form_id}_edit_mode"] = True
                    st.rerun()
            else:
                if st.button("💾 Salvar", use_container_width=True):
                    if self.save():
                        st.success("Formulário salvo com sucesso!")
                        if not self._is_form_empty():
                            st.session_state[f"{self.form_id}_edit_mode"] = False
                        st.rerun()
        
        # Adiciona seção de debug após o cabeçalho
        self._render_debug_section()
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        Deve ser implementado pelas classes filhas.
        """
        raise NotImplementedError 