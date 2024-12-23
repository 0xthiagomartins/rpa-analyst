import pytest
import os
from unittest.mock import patch, Mock
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

def test_create_template_env(document_service):
    """Testa se o ambiente de template é criado corretamente."""
    assert document_service.template_env is not None
    template = document_service.template_env.get_template('pdd.html')
    assert template is not None

@patch('weasyprint.HTML')
def test_generate_pdd(mock_weasyprint, document_service, sample_pdd_data):
    """Testa a geração do PDD."""
    # Configura o mock
    mock_html = Mock()
    mock_weasyprint.return_value = mock_html
    
    # Gera o documento
    pdf_path = document_service.generate_pdd(sample_pdd_data)
    
    # Verifica se o arquivo HTML foi criado
    assert os.path.exists(pdf_path.replace('.pdf', '.html'))
    
    # Verifica se weasyprint foi chamado
    mock_weasyprint.assert_called_once()
    mock_html.write_pdf.assert_called_once()
    
    # Limpa os arquivos gerados
    os.remove(pdf_path.replace('.pdf', '.html'))

def test_generate_pdd_invalid_data(document_service):
    """Testa a geração do PDD com dados inválidos."""
    with pytest.raises(ValueError):
        document_service.generate_pdd({}) 