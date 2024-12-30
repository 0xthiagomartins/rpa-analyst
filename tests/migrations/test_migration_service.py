"""Testes para o serviço de migração."""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.migrations.migration_service import MigrationService
from src.migrations.feature_flags import MigrationFlag

@pytest.fixture
def migration_service():
    """Fixture que cria uma instância do serviço de migração."""
    return MigrationService()

@pytest.fixture
def sample_data():
    """Fixture com dados de exemplo para migração."""
    return {
        "name": "Test Process",
        "description": "Test Description",
        "steps": ["Step 1", "Step 2"]
    }

def test_start_migration_success(migration_service, sample_data, tmp_path):
    """Testa migração bem sucedida."""
    # Mock do backup service
    backup_file = tmp_path / "backup.json"
    backup_file.touch()
    migration_service.backup_service.create_backup = Mock(return_value=backup_file)
    
    # Mock do mapeamento
    migration_service._map_data = Mock(return_value={"migrated": True})
    
    # Mock da validação
    migration_service._validate_migration = Mock(return_value=True)
    
    result = migration_service.start_migration("identification", sample_data)
    
    assert result is True
    migration_service.backup_service.create_backup.assert_called_once()
    migration_service._map_data.assert_called_once()
    migration_service._validate_migration.assert_called_once()

def test_start_migration_backup_failure(migration_service, sample_data):
    """Testa falha no backup durante migração."""
    migration_service.backup_service.create_backup = Mock(return_value=None)
    
    result = migration_service.start_migration("identification", sample_data)
    
    assert result is False
    migration_service.backup_service.create_backup.assert_called_once()
    
def test_start_migration_mapping_failure(migration_service, sample_data, tmp_path):
    """Testa falha no mapeamento durante migração."""
    # Mock do backup service
    backup_file = tmp_path / "backup.json"
    backup_file.touch()
    migration_service.backup_service.create_backup = Mock(return_value=backup_file)
    
    # Mock do mapeamento com falha
    migration_service._map_data = Mock(return_value=None)
    
    result = migration_service.start_migration("identification", sample_data)
    
    assert result is False
    migration_service.backup_service.create_backup.assert_called_once()
    migration_service._map_data.assert_called_once()

def test_start_migration_validation_failure(migration_service, sample_data, tmp_path):
    """Testa falha na validação durante migração."""
    # Mock do backup service
    backup_file = tmp_path / "backup.json"
    backup_file.touch()
    migration_service.backup_service.create_backup = Mock(return_value=backup_file)
    
    # Mock do mapeamento
    migration_service._map_data = Mock(return_value={"migrated": True})
    
    # Mock da validação com falha
    migration_service._validate_migration = Mock(return_value=False)
    
    result = migration_service.start_migration("identification", sample_data)
    
    assert result is False
    migration_service.backup_service.create_backup.assert_called_once()
    migration_service._map_data.assert_called_once()
    migration_service._validate_migration.assert_called_once()

def test_rollback_migration_success(migration_service, sample_data, tmp_path):
    """Testa rollback bem sucedido."""
    backup_file = tmp_path / "backup.json"
    backup_file.touch()
    
    # Mock da restauração do backup
    migration_service.backup_service.restore_backup = Mock(return_value=sample_data)
    
    result = migration_service.rollback_migration("identification", backup_file)
    
    assert result is True
    migration_service.backup_service.restore_backup.assert_called_once()
    assert not migration_service.feature_flags.is_enabled(MigrationFlag.IDENTIFICATION_MIGRATED)

def test_rollback_migration_failure(migration_service, tmp_path):
    """Testa falha no rollback."""
    backup_file = tmp_path / "backup.json"
    backup_file.touch()
    
    # Mock da restauração do backup com falha
    migration_service.backup_service.restore_backup = Mock(return_value=None)
    
    result = migration_service.rollback_migration("identification", backup_file)
    
    assert result is False
    migration_service.backup_service.restore_backup.assert_called_once()

def test_get_migration_status(migration_service):
    """Testa obtenção do status da migração."""
    # Ativa alguns flags
    migration_service.feature_flags.enable(MigrationFlag.IDENTIFICATION_MIGRATED)
    migration_service.feature_flags.enable(MigrationFlag.PROCESS_DETAILS_MIGRATED)
    
    status = migration_service.get_migration_status()
    
    assert status[MigrationFlag.IDENTIFICATION_MIGRATED.value] is True
    assert status[MigrationFlag.PROCESS_DETAILS_MIGRATED.value] is True
    assert status[MigrationFlag.BUSINESS_RULES_MIGRATED.value] is False

def test_invalid_form_name(migration_service, sample_data):
    """Testa migração com nome de formulário inválido."""
    result = migration_service.start_migration("invalid_form", sample_data)
    assert result is False 