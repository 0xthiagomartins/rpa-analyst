"""Sistema de roteamento da aplicação."""
from typing import Dict, Type, Optional
import streamlit as st
from utils.dependency_container import DependencyContainer
from views.pages.base_page import BasePage

class Router:
    """Gerencia o roteamento entre páginas da aplicação."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """
        Inicializa o router.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container or DependencyContainer()
        self.routes: Dict[str, Type[BasePage]] = {}
    
    def register_routes(self, routes: Dict[str, Type[BasePage]]) -> None:
        """
        Registra as rotas disponíveis.
        
        Args:
            routes: Dicionário de rotas
        """
        self.routes = routes
    
    def get_current_page(self) -> str:
        """
        Obtém a página atual da URL.
        
        Returns:
            str: Path da página atual
        """
        return st.query_params.get("page", "/")
    
    def get_current_process_id(self) -> Optional[str]:
        """
        Obtém o ID do processo atual da URL.
        
        Returns:
            Optional[str]: ID do processo ou None
        """
        return st.query_params.get("process_id")
    
    def navigate(self, url: str, process_id: Optional[str] = None) -> None:
        """
        Navega para uma nova URL.
        
        Args:
            url: URL de destino
            process_id: ID do processo opcional
        """
        st.query_params["page"] = url
        if process_id:
            st.query_params["process_id"] = process_id
        else:
            st.query_params.pop("process_id", None)
    
    def render(self) -> None:
        """Renderiza a página atual."""
        current_page = self.get_current_page()
        page_class = self.routes.get(current_page)
        
        if page_class:
            page = page_class(self.container)
            page.render()
        else:
            st.error("404 - Página não encontrada")
            if st.button("Voltar para Home"):
                self.navigate("/") 