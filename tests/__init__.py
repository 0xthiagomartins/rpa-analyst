import os
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Não precisa importar do tests/conftest.py pois o pytest encontrará automaticamente
