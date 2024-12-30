"""Testes para o serviço de backup."""
import pytest
import json
from pathlib import Path
from datetime import datetime
from src.migrations.backup_service import BackupService

@pytest.fixture
def backup_dir(tmp_path):
    """Fixture que cria um diretório temporário para backups."""
    return str(tmp_path / "backups")

@pytest.fixture
def backup_service(backup_dir):
    """Fixture que cria uma instância do serviço de backup."""
    return BackupService(backup_dir)

@pytest.fixture
def sample_data():
    """Fixture com dados de exemplo para backup."""
    return {
        "name": "Test Process",
        "description": "Test Description",
        "steps": ["Step 1", "Step 2"]
    }

def test_create_backup(backup_service, sample_data):
    """Testa criação de backup."""
    backup_file = backup_service.create_backup("test_form", sample_data)
    
    assert backup_file is not None
    assert backup_file.exists()
    
    # Verifica conteúdo
    with open(backup_file) as f:
        restored_data = json.load(f)
    assert restored_data == sample_data

def test_restore_backup(backup_service, sample_data):
    """Testa restauração de backup."""
    backup_file = backup_service.create_backup("test_form", sample_data)
    restored_data = backup_service.restore_backup(backup_file)
    
    assert restored_data == sample_data

def test_list_backups(backup_service, sample_data):
    """Testa listagem de backups."""
    # Cria alguns backups
    backup_service.create_backup("form1", sample_data)
    backup_service.create_backup("form1", sample_data)
    backup_service.create_backup("form2", sample_data)
    
    # Lista todos os backups
    all_backups = backup_service.list_backups()
    assert len(all_backups) == 2
    assert len(all_backups["form1"]) == 2
    assert len(all_backups["form2"]) == 1
    
    # Lista backups de um formulário específico
    form1_backups = backup_service.list_backups("form1")
    assert len(form1_backups["form1"]) == 2

def test_cleanup_old_backups(backup_service, sample_data):
    """Testa limpeza de backups antigos."""
    # Cria vários backups
    for _ in range(7):
        backup_service.create_backup("test_form", sample_data)
    
    # Limpa mantendo apenas 5
    backup_service.cleanup_old_backups(max_backups=5)
    
    # Verifica se apenas 5 permaneceram
    backups = backup_service.list_backups("test_form")
    assert len(backups["test_form"]) == 5

def test_failed_backup(backup_service, monkeypatch):
    """Testa falha na criação de backup."""
    def mock_open(*args, **kwargs):
        raise IOError("Simulated error")
    
    monkeypatch.setattr("builtins.open", mock_open)
    result = backup_service.create_backup("test_form", {})
    
    assert result is None

def test_failed_restore(backup_service):
    """Testa falha na restauração de backup."""
    result = backup_service.restore_backup(Path("nonexistent.json"))
    assert result is None 