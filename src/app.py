"""Ponto de entrada da aplicação."""
import streamlit as st
from views.router import Router
from views.pages.main_page import MainPage
from utils.dependency_container import DependencyContainer

def setup_page() -> None:
    """Configura a página do Streamlit."""
    st.set_page_config(
        page_title="Agente Analista de RPA",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplica estilos CSS
    st.markdown("""
        <style>
            .main-header {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 2rem;
            }
            .section-header {
                font-size: 1.5rem;
                font-weight: bold;
                margin: 1rem 0;
            }
            .stButton>button {
                width: 100%;
            }
            .status-box {
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Função principal da aplicação."""
    # Configura a página (deve ser o primeiro comando Streamlit)
    setup_page()
    
    # Inicializa container de dependências
    container = DependencyContainer()
    
    # Inicializa router e registra rotas
    router = Router(container)
    router.register_routes({
        "/": MainPage,
        "/process/new": MainPage,
        "/process/view": MainPage,
    })
    
    # Renderiza a página atual
    router.render()

if __name__ == "__main__":
    main()
