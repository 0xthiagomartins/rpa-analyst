import pytest
import os
from unittest.mock import patch
from src.services.document_service import DocumentService

@pytest.fixture
def sample_pdd_data():
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
def document_service():
    return DocumentService()

def test_ensure_output_dir(document_service):
    """Testa se o diretório de saída é criado corretamente."""
    assert os.path.exists(document_service.output_dir)
    assert os.path.isdir(document_service.output_dir)

def test_validate_data(document_service):
    """Testa a validação dos dados."""
    with pytest.raises(ValueError):
        document_service.generate_pdd({})

@patch('reportlab.platypus.SimpleDocTemplate')
def test_generate_pdd(mock_doc, document_service, sample_pdd_data):
    """Testa a geração do PDD."""
    # Configura o mock
    mock_doc.return_value.build.return_value = None
    
    # Gera o documento
    pdf_path = document_service.generate_pdd(sample_pdd_data)
    
    # Verifica se o caminho foi gerado corretamente
    assert pdf_path.endswith('.pdf')
    assert 'PDD_Processo_de_Teste_' in pdf_path 