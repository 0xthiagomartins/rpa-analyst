"""Testes para as constantes do módulo de processo."""
import pytest
from src.views.components.process.config.constants import (
    ERROR_MESSAGES,
    UI_CONFIG
)

def test_error_messages_exist():
    """Testa se as mensagens de erro existem."""
    assert 'REQUIRED_FIELD' in ERROR_MESSAGES
    assert 'INVALID_FORMAT' in ERROR_MESSAGES
    assert 'SAVE_ERROR' in ERROR_MESSAGES

def test_error_messages_format():
    """Testa o formato das mensagens de erro."""
    for message in ERROR_MESSAGES.values():
        assert isinstance(message, str)
        assert message.strip() != ""

def test_ui_config_exists():
    """Testa se as configurações de UI existem."""
    assert 'MAX_NAME_LENGTH' in UI_CONFIG
    assert 'MAX_DESCRIPTION_LENGTH' in UI_CONFIG
    assert 'DEFAULT_HEIGHT' in UI_CONFIG
    assert 'COLUMN_WIDTHS' in UI_CONFIG

def test_ui_config_values():
    """Testa os valores das configurações de UI."""
    assert UI_CONFIG['MAX_NAME_LENGTH'] > 0
    assert UI_CONFIG['MAX_DESCRIPTION_LENGTH'] > 0
    assert UI_CONFIG['DEFAULT_HEIGHT'] > 0
    assert 'DEFAULT' in UI_CONFIG['COLUMN_WIDTHS']
    assert 'UNEVEN' in UI_CONFIG['COLUMN_WIDTHS'] 