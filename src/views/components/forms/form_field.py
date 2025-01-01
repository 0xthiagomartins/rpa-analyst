"""Componente para campos de formulário com controle de edição."""
from typing import Any, Optional, Callable
import streamlit as st
from views.components.state.state_manager import StateManager, FormState

class FormField:
    """Campo de formulário com controle de edição."""
    
    def __init__(self, form_id: str, field_id: str):
        self.form_id = form_id
        self.field_id = field_id
        self.state_manager = StateManager()
    
    def render_text_input(
        self,
        label: str,
        value: str,
        is_disabled: bool,
        help: Optional[str] = None,
        key: Optional[str] = None
    ) -> str:
        """
        Renderiza um campo de texto.
        
        Args:
            label: Label do campo
            value: Valor atual
            is_disabled: Se o campo está desabilitado
            help: Texto de ajuda
            key: Chave única para o campo
            
        Returns:
            str: Valor atual do campo
        """
        return st.text_input(
            label,
            value=value,
            disabled=is_disabled,
            help=help,
            key=key or f"{self.form_id}_{self.field_id}"
        )
    
    def render_text_area(
        self,
        label: str,
        value: str,
        is_disabled: bool,
        help: Optional[str] = None,
        key: Optional[str] = None,
        height: int = 100
    ) -> str:
        """
        Renderiza uma área de texto.
        
        Args:
            label: Label do campo
            value: Valor atual
            is_disabled: Se o campo está desabilitado
            help: Texto de ajuda
            key: Chave única para o campo
            height: Altura do campo
            
        Returns:
            str: Valor atual do campo
        """
        return st.text_area(
            label,
            value=value,
            disabled=is_disabled,
            help=help,
            height=height,
            key=key or f"{self.form_id}_{self.field_id}"
        ) 