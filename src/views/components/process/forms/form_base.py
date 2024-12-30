"""Módulo base para formulários."""
from typing import Optional, Dict, Any
import streamlit as st
from src.utils.dependency_container import DependencyContainer
from src.utils.validators import FormValidator

class FormBase:
    """Classe base para formulários do processo."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa o formulário base."""
        self.container = container or DependencyContainer()
        self.validator = self.container.resolve(FormValidator)
        self._data: Dict[str, Any] = {}
        
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        raise NotImplementedError
        
    def render(self) -> None:
        """Renderiza o formulário."""
        raise NotImplementedError
        
    @property
    def data(self) -> Dict[str, Any]:
        """Retorna os dados do formulário."""
        return self._data.copy() 