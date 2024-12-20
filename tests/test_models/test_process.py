import pytest
from src.models.process import Process

def test_process_creation(sample_process_data):
    """Testa a criação de um processo a partir de um dicionário."""
    process = Process.from_dict(sample_process_data)
    
    assert process.name == sample_process_data['process_name']
    assert process.owner == sample_process_data['process_owner']
    assert process.description == sample_process_data['process_description']

def test_process_to_dict(sample_process_data):
    """Testa a conversão de um processo para dicionário."""
    process = Process.from_dict(sample_process_data)
    data = process.to_dict()
    
    assert data['process_name'] == sample_process_data['process_name']
    assert data['process_owner'] == sample_process_data['process_owner']
    assert data['process_description'] == sample_process_data['process_description']

def test_process_empty_fields():
    """Testa a criação de um processo com campos vazios."""
    empty_data = {}
    process = Process.from_dict(empty_data)
    
    assert process.name == ''
    assert process.owner == ''
    assert process.description == '' 