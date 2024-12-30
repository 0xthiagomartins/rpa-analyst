"""Testes de integração para o processo de migração."""
import pytest
from datetime import datetime
from src.migrations.migration_service import MigrationService
from src.migrations.data_mapper import DataMapper
from src.migrations.validators import DataValidator

@pytest.fixture
def migration_service():
    """Fixture que retorna uma instância do MigrationService."""
    return MigrationService(DataMapper(), DataValidator())

@pytest.fixture
def sample_old_identification_data():
    """Fixture com dados antigos de exemplo."""
    return {
        "name": "Processo de Vendas",
        "id": "PROC-001",
        "department": "Comercial",
        "owner": "João Silva",
        "participants": ["Maria Santos", "Pedro Costa"],
        "created_at": "2024-01-01",
        "updated_at": "2024-01-15",
        "status": "draft"
    }

def test_identification_form_migration_success(migration_service, sample_old_identification_data):
    """Testa migração bem sucedida do IdentificationForm."""
    # Executa migração
    result = migration_service.migrate_identification_form(sample_old_identification_data)
    
    # Verifica sucesso
    assert result["success"] is True
    assert result["errors"] == []
    
    # Verifica dados migrados
    migrated_data = result["data"]
    assert migrated_data["process_name"] == "Processo de Vendas"
    assert migrated_data["process_id"] == "PROC-001"
    assert migrated_data["department"] == "Comercial"
    assert migrated_data["owner"] == "João Silva"
    assert len(migrated_data["participants"]) == 2
    assert migrated_data["creation_date"] == "2024-01-01"
    assert migrated_data["last_update"] == "2024-01-15"
    assert migrated_data["status"] == "draft"

def test_identification_form_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos."""
    invalid_data = {
        "name": "",  # Nome vazio (inválido)
        "id": "invalid-id",  # ID com formato inválido
        "status": "invalid"  # Status inválido
    }
    
    result = migration_service.migrate_identification_form(invalid_data)
    
    # Verifica falha
    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert any("process_name" in error for error in result["errors"])
    assert any("process_id" in error for error in result["errors"])
    assert any("status" in error for error in result["errors"])

def test_identification_form_migration_rollback(migration_service, sample_old_identification_data):
    """Testa rollback da migração em caso de erro."""
    # Simula erro durante salvamento
    migration_service.save_error = True
    
    result = migration_service.migrate_identification_form(sample_old_identification_data)
    
    # Verifica falha e rollback
    assert result["success"] is False
    assert "rollback" in result
    assert result["rollback"]["success"] is True 