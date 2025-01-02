"""Módulo de inicialização da aplicação."""
import os
import sys
from pathlib import Path
import asyncio
import nest_asyncio

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Permite nested event loops (necessário para Streamlit + asyncio)
nest_asyncio.apply()

# Importa a função main
from app import main

if __name__ == "__main__":
    main()
