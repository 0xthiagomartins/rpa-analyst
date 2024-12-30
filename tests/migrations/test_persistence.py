"""Testes para o módulo de persistência."""
import pytest
import json
from pathlib import Path
from src.migrations.persistence import MigrationPersistence

@pytest.fixture
def persistence():
    """Fixture que retorna uma instância do MigrationPersistence."""
    # Usa pasta temporária para testes
    return MigrationPersistence(storage_path="tests/data/migrations")

@pytest.fixture
def sample_identification_data():
    """Fixture com dados de exemplo."""
    return {
        "process_name": "Test Process",
        "process_id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "draft"
    }

def test_save_identification_form(persistence, sample_identification_data):
    """Testa salvamento bem sucedido."""
    result = persistence.save_identification_form(
        sample_identification_data,
        "PROC-001"
    )
    
    assert result["success"] is True
    
    # Verifica se arquivo foi criado
    file_path = Path("tests/data/migrations/PROC-001/identification.json")
    assert file_path.exists()
    
    # Verifica conteúdo
    with open(file_path, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        assert saved_data["data"] == sample_identification_data
        assert "metadata" in saved_data

def test_load_identification_form(persistence, sample_identification_data):
    """Testa carregamento bem sucedido."""
    # Salva dados primeiro
    persistence.save_identification_form(sample_identification_data, "PROC-001")
    
    # Carrega dados
    loaded_data = persistence.load_identification_form("PROC-001")
    
    assert loaded_data is not None
    assert loaded_data["data"] == sample_identification_data

def test_delete_identification_form(persistence, sample_identification_data):
    """Testa remoção bem sucedida."""
    # Salva dados primeiro
    persistence.save_identification_form(sample_identification_data, "PROC-001")
    
    # Remove dados
    result = persistence.delete_identification_form("PROC-001")
    
    assert result["success"] is True
    
    # Verifica se arquivo foi removido
    file_path = Path("tests/data/migrations/PROC-001/identification.json")
    assert not file_path.exists() 