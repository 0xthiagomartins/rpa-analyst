"""Gerenciador de estado da aplicação."""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import streamlit as st
from enum import Enum

class FormState(Enum):
    """Estados possíveis de um formulário."""
    EMPTY = "empty"
    EDITING = "editing"
    INVALID = "invalid"
    COMPLETED = "completed"

@dataclass
class FormData:
    """Dados de um formulário."""
    data: Dict[str, Any]
    is_valid: bool = False
    state: FormState = FormState.EMPTY

class StateManager:
    """Gerenciador de estado da aplicação."""
    
    def __init__(self):
        """Inicializa o gerenciador de estado."""
        if 'current_form' not in st.session_state:
            st.session_state.current_form = "identification"
            
        if 'forms_data' not in st.session_state:
            st.session_state.forms_data = {}
    
    def get_current_form(self) -> str:
        """
        Obtém o formulário atual.
        
        Returns:
            str: ID do formulário atual
        """
        return st.session_state.current_form
    
    def navigate_to(self, form_id: str) -> None:
        """
        Navega para um formulário específico.
        
        Args:
            form_id: ID do formulário
        """
        st.session_state.current_form = form_id
    
    def get_form_data(self, form_id: str) -> FormData:
        """
        Obtém os dados de um formulário.
        
        Args:
            form_id: ID do formulário
            
        Returns:
            FormData: Dados do formulário
        """
        if form_id not in st.session_state.forms_data:
            return FormData({}, False, FormState.EMPTY)
        return st.session_state.forms_data[form_id]
    
    def update_form_data(
        self, 
        form_id: str, 
        data: Dict[str, Any], 
        is_valid: bool = False,
        state: Optional[FormState] = None
    ) -> None:
        """
        Atualiza os dados de um formulário.
        
        Args:
            form_id: ID do formulário
            data: Novos dados
            is_valid: Se os dados são válidos
            state: Estado opcional do formulário
        """
        if state is None:
            if not data:
                state = FormState.EMPTY
            elif not is_valid:
                state = FormState.INVALID
            else:
                state = FormState.COMPLETED
        
        st.session_state.forms_data[form_id] = FormData(
            data=data,
            is_valid=is_valid,
            state=state
        )
    
    def clear_form(self, form_id: str) -> None:
        """
        Limpa os dados de um formulário.
        
        Args:
            form_id: ID do formulário
        """
        if form_id in st.session_state.forms_data:
            del st.session_state.forms_data[form_id]
    
    def clear_all(self) -> None:
        """Limpa todos os dados."""
        st.session_state.forms_data = {}
        st.session_state.current_form = "identification" 