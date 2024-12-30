"""Testes para o gerenciador de feature flags."""
import pytest
from pathlib import Path
import json
from src.migrations.feature_flags import FeatureFlagManager, MigrationFlag

@pytest.fixture
def temp_config(tmp_path):
    """Fixture que cria um arquivo de configuração temporário."""
    config_file = tmp_path / "feature_flags.json"
    return str(config_file)

@pytest.fixture
def flag_manager(temp_config):
    """Fixture que cria uma instância do gerenciador."""
    return FeatureFlagManager(temp_config)

def test_initialization(temp_config):
    """Testa inicialização do gerenciador."""
    manager = FeatureFlagManager(temp_config)
    
    # Verifica se arquivo foi criado
    assert Path(temp_config).exists()
    
    # Verifica se todos os flags foram inicializados como False
    with open(temp_config) as f:
        flags = json.load(f)
    
    assert all(not value for value in flags.values())
    assert len(flags) == len(MigrationFlag)

def test_enable_flag(flag_manager):
    """Testa ativação de flag."""
    flag_manager.enable(MigrationFlag.USE_NEW_FORMS)
    assert flag_manager.is_enabled(MigrationFlag.USE_NEW_FORMS)

def test_disable_flag(flag_manager):
    """Testa desativação de flag."""
    flag_manager.enable(MigrationFlag.USE_NEW_FORMS)
    flag_manager.disable(MigrationFlag.USE_NEW_FORMS)
    assert not flag_manager.is_enabled(MigrationFlag.USE_NEW_FORMS)

def test_reset_all(flag_manager):
    """Testa reset de todos os flags."""
    # Ativa alguns flags
    flag_manager.enable(MigrationFlag.USE_NEW_FORMS)
    flag_manager.enable(MigrationFlag.IDENTIFICATION_MIGRATED)
    
    # Reseta todos
    flag_manager.reset_all()
    
    # Verifica se todos estão desativados
    assert all(not value for value in flag_manager.status.values())

def test_status(flag_manager):
    """Testa obtenção do status dos flags."""
    flag_manager.enable(MigrationFlag.USE_NEW_FORMS)
    status = flag_manager.status
    
    assert status[MigrationFlag.USE_NEW_FORMS.value]
    assert not status[MigrationFlag.IDENTIFICATION_MIGRATED.value]

def test_persistence(temp_config):
    """Testa persistência dos flags entre instâncias."""
    # Primeira instância
    manager1 = FeatureFlagManager(temp_config)
    manager1.enable(MigrationFlag.USE_NEW_FORMS)
    
    # Segunda instância
    manager2 = FeatureFlagManager(temp_config)
    assert manager2.is_enabled(MigrationFlag.USE_NEW_FORMS) 