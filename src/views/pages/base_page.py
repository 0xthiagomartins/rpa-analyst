"""Classe base para páginas da aplicação."""
from abc import ABC, abstractmethod
from typing import Optional
from utils.dependency_container import DependencyContainer

class BasePage(ABC):
    """Classe base para todas as páginas."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """
        Inicializa a página base.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container or DependencyContainer()
    
    @abstractmethod
    def render(self) -> None:
        """Renderiza a página."""
        pass 