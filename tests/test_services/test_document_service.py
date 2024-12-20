import pytest
import os
from src.services.document_service import DocumentService
from src.models.process import Process

@pytest.fixture
def document_service():
    return DocumentService()

def test_generate_html(document_service, sample_process_data):
    """Testa a geração de HTML."""
    process = Process.from_dict(sample_process_data)
    html = document_service.generate_html(process)
    
    assert isinstance(html, str)
    assert process.name in html
    assert process.owner in html
    assert process.description in html

@pytest.mark.skipif(
    not DocumentService()._get_wkhtmltopdf_path(),
    reason="wkhtmltopdf não está instalado"
)
def test_generate_pdf(document_service, sample_process_data):
    """Testa a geração de PDF."""
    process = Process.from_dict(sample_process_data)
    pdf_path = document_service.generate_pdf(process)
    
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith('.pdf')
    expected_prefix = f"PDD_{process.name.replace(' ', '_')}"
    assert os.path.basename(pdf_path).startswith(expected_prefix)

@pytest.mark.skipif(
    not DocumentService()._get_wkhtmltopdf_path(),
    reason="wkhtmltopdf não está instalado"
)
def test_get_document_path(document_service, sample_process_data):
    """Testa a recuperação do caminho do documento."""
    process = Process.from_dict(sample_process_data)
    
    # Primeiro, gera um PDF
    pdf_path = document_service.generate_pdf(process)
    
    # Depois tenta recuperar o caminho
    retrieved_path = document_service.get_document_path(process.name.replace(' ', '_'))
    assert retrieved_path == pdf_path

def test_invalid_process_data(document_service):
    """Testa a geração com dados inválidos."""
    invalid_data = {'process_name': 'Test'}
    process = Process.from_dict(invalid_data)
    
    if document_service.wkhtmltopdf:
        with pytest.raises(ValueError):
            document_service.generate_pdf(process)
    else:
        with pytest.raises(RuntimeError):
            document_service.generate_pdf(process) 