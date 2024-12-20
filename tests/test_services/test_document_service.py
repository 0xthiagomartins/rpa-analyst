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

def test_generate_pdf(document_service, sample_process_data):
    """Testa a geração de PDF."""
    process = Process.from_dict(sample_process_data)
    pdf_path = document_service.generate_pdf(process)
    
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith('.pdf')
    assert os.path.basename(pdf_path).startswith(f"PDD_{process.name}")

def test_get_document_path(document_service, sample_process_data):
    """Testa a recuperação do caminho do documento."""
    process = Process.from_dict(sample_process_data)
    
    # Primeiro, gera um PDF
    pdf_path = document_service.generate_pdf(process)
    
    # Depois tenta recuperar o caminho
    retrieved_path = document_service.get_document_path(process.name)
    assert retrieved_path == pdf_path

def test_invalid_process_data(document_service):
    """Testa a geração com dados inválidos."""
    invalid_data = {'process_name': 'Test'}
    process = Process.from_dict(invalid_data)
    
    with pytest.raises(ValueError):
        document_service.generate_pdf(process) 