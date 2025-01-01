"""Módulo para gerenciamento de erros da interface."""
from typing import Dict, Any, List, Optional
import streamlit as st
from dataclasses import dataclass
from enum import Enum

class ErrorLevel(Enum):
    """Níveis de erro possíveis."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ErrorMessage:
    """Classe para representar uma mensagem de erro."""
    message: str
    level: ErrorLevel
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class ErrorHandler:
    """Gerenciador de erros da interface."""
    
    def __init__(self):
        """Inicializa o gerenciador de erros."""
        if 'errors' not in st.session_state:
            st.session_state['errors'] = []
    
    def add_error(self, message: str, level: ErrorLevel = ErrorLevel.ERROR, 
                 field: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
        """Adiciona um erro ao estado."""
        if 'errors' not in st.session_state:
            st.session_state['errors'] = []
        
        error = ErrorMessage(
            message=message,
            level=level,
            field=field,
            details=details
        )
        st.session_state['errors'].append(error)
    
    def get_errors(self, level: Optional[ErrorLevel] = None) -> List[ErrorMessage]:
        """Retorna erros filtrados por nível."""
        if 'errors' not in st.session_state:
            return []
            
        if level is None:
            return st.session_state['errors']
            
        return [e for e in st.session_state['errors'] if e.level == level]
    
    def clear_errors(self, level: Optional[ErrorLevel] = None) -> None:
        """Limpa erros do estado."""
        if level is None:
            st.session_state['errors'] = []
        else:
            st.session_state['errors'] = [
                e for e in st.session_state['errors'] 
                if e.level != level
            ]
    
    def has_errors(self, level: Optional[ErrorLevel] = None) -> bool:
        """Verifica se existem erros."""
        return len(self.get_errors(level)) > 0
    
    def render_errors(self, level: Optional[ErrorLevel] = None) -> None:
        """Renderiza erros na interface."""
        errors = self.get_errors(level)
        if not errors:
            return
            
        for error in errors:
            if error.level == ErrorLevel.INFO:
                st.info(error.message)
            elif error.level == ErrorLevel.WARNING:
                st.warning(error.message)
            elif error.level == ErrorLevel.ERROR:
                st.error(error.message)
            elif error.level == ErrorLevel.CRITICAL:
                st.error(f"🚨 {error.message}")
                
            if error.field:
                st.caption(f"Campo: {error.field}")
            if error.details:
                with st.expander("Detalhes"):
                    st.json(error.details) 