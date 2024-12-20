import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
src_dir = os.path.join(parent_dir, "src")
sys.path.insert(0, src_dir)

import pytest
from src.models.process import Process
from src.controllers.process_controller import ProcessController
from src.utils.config import Config
from src.utils.validators import FormValidator

@pytest.fixture
def sample_process_data():
    """Fixture que fornece dados de exemplo para um processo."""
    return {
        'process_name': 'Processo de Teste',
        'process_owner': 'João Silva',
        'process_description': 'Descrição do processo de teste',
        'steps_as_is': 'Passo 1\nPasso 2\nPasso 3',
        'systems': 'Sistema A, Sistema B',
        'data_used': 'Dados X, Dados Y',
        'business_rules': 'Regra 1\nRegra 2',
        'exceptions': 'Exceção 1\nExceção 2',
        'automation_goals': 'Objetivo 1\nObjetivo 2',
        'kpis': 'KPI 1\nKPI 2'
    }

@pytest.fixture
def process_controller():
    """Fixture que fornece uma instância do ProcessController."""
    return ProcessController()

@pytest.fixture
def form_validator():
    """Fixture que fornece uma instância do FormValidator."""
    return FormValidator()

@pytest.fixture
def config():
    """Fixture que fornece uma instância de Config."""
    return Config() 