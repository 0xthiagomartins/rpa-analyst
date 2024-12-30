"""Testes para o serviço de migração."""
import pytest
from datetime import datetime
from src.migrations.migration_service import MigrationService
from src.migrations.data_mapper import DataMapper
from src.migrations.validators import DataValidator
from src.migrations.backup_service import BackupService

@pytest.fixture
def migration_service():
    """Fixture que cria uma instância do serviço de migração."""
    mapper = DataMapper()
    validator = DataValidator()
    return MigrationService(mapper=mapper, validator=validator)

def test_start_migration_success(migration_service):
    """Testa início bem sucedido da migração."""
    form_name = "identification"
    old_data = {
        "name": "Test Process",
        "id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "draft"
    }
    
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is True
    assert not result["errors"]
    assert result["data"] is not None

def test_start_migration_backup_failure(migration_service, monkeypatch):
    """Testa falha no backup antes da migração."""
    def mock_backup_error(*args, **kwargs):
        raise Exception("Backup failed")
    
    monkeypatch.setattr(BackupService, "create_backup", mock_backup_error)
    
    old_data = {
        "name": "Test Process",
        "id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "draft"
    }
    
    migration_service.save_error = True
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert result["rollback"]["success"] is True

def test_start_migration_mapping_failure(migration_service, monkeypatch):
    """Testa falha no mapeamento dos dados."""
    def mock_mapping_error(*args, **kwargs):
        raise Exception("Mapping failed")
    
    monkeypatch.setattr(DataMapper, "map_identification_data", mock_mapping_error)
    
    old_data = {
        "name": "Test Process",
        "id": "PROC-001"
    }
    
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is False
    assert "Mapping failed" in str(result["errors"])

def test_start_migration_validation_failure(migration_service):
    """Testa falha na validação dos dados."""
    old_data = {
        "name": "",  # Nome vazio (inválido)
        "id": "invalid-id",  # ID com formato inválido
        "status": "invalid"  # Status inválido
    }
    
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is False
    assert len(result["errors"]) > 0

def test_rollback_migration_success(migration_service):
    """Testa rollback bem sucedido."""
    old_data = {
        "name": "Test Process",
        "id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "draft"
    }
    
    migration_service.save_error = True
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is False
    assert result["rollback"]["success"] is True

def test_rollback_migration_failure(migration_service, monkeypatch):
    """Testa falha no rollback."""
    def mock_rollback_error(*args, **kwargs):
        raise Exception("Rollback failed")
    
    monkeypatch.setattr(MigrationService, "_rollback_identification_form", mock_rollback_error)
    
    old_data = {
        "name": "Test Process",
        "id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "draft"
    }
    
    migration_service.save_error = True
    result = migration_service.migrate_identification_form(old_data)
    
    assert result["success"] is False
    assert "Rollback failed" in str(result["errors"])

def test_get_migration_status(migration_service):
    """Testa obtenção do status da migração."""
    form_name = "identification"
    old_data = {
        "name": "Test Process",
        "id": "PROC-001"
    }
    
    # Inicia migração
    migration_service.migrate_identification_form(old_data)
    
    # Verifica status
    status = migration_service.get_migration_status(form_name)
    assert isinstance(status, dict)
    assert "status" in status
    assert "details" in status

def test_invalid_form_name(migration_service):
    """Testa tentativa de migração com nome de formulário inválido."""
    form_name = "invalid_form"
    old_data = {"name": "Test"}
    
    with pytest.raises(ValueError, match="Invalid form name"):
        migration_service.get_migration_status(form_name) 