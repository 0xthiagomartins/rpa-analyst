"""Módulo de inicialização da aplicação."""
import os
import sys
from pathlib import Path
import asyncio
import nest_asyncio
import streamlit as st

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Enable nested asyncio for Streamlit
nest_asyncio.apply()

# Import após adicionar root ao path
from src.views.main_view import MainView

async def main():
    """Função principal da aplicação."""
    st.set_page_config(
        page_title="RPA Analyst",
        page_icon="🤖",
        layout="wide"
    )
    
    view = MainView()
    await view.render()

if __name__ == "__main__":
    asyncio.run(main())
