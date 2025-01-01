"""Testes para o ValidationSummary."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.validation.validation_summary import (
    ValidationSummary,
    ValidationStatus,
    FormValidation
)
from src.views.components.state.state_manager import FormState
from src.views.components.error.error_handler import ErrorLevel, ErrorMessage

@pytest.fixture
def mock_state_manager():
    """Mock para o StateManager."""
    manager = Mock()
    # Simula um formulário válido
    form_data = Mock(
        data={"field": "value"},
        is_valid=True,
        state=FormState.COMPLETED
    )
    manager.get_form_data.return_value = form_data
    return manager

@pytest.fixture
def mock_error_handler():
    """Mock para o ErrorHandler."""
    handler = Mock()
    handler.get_errors.return_value = []
    return handler

@pytest.fixture
def validation_summary(mock_state_manager, mock_error_handler):
    """Fixture que retorna um ValidationSummary configurado para testes."""
    return ValidationSummary(
        state_manager=mock_state_manager,
        error_handler=mock_error_handler
    )

def test_get_form_validation_valid(validation_summary):
    """Testa obtenção de validação para formulário válido."""
    validation = validation_summary.get_form_validation("identification")
    
    assert validation.form_id == "identification"
    assert validation.title == "Identificação"
    assert validation.status == ValidationStatus.VALID
    assert not validation.errors
    assert not validation.warnings

def test_get_form_validation_with_errors(validation_summary, mock_error_handler):
    """Testa obtenção de validação com erros."""
    # Simula erros no formulário
    mock_error_handler.get_errors.return_value = [
        ErrorMessage("Erro 1", ErrorLevel.ERROR, field="identification.field1"),
        ErrorMessage("Erro 2", ErrorLevel.ERROR, field="identification.field2")
    ]
    
    validation = validation_summary.get_form_validation("identification")
    
    assert validation.status == ValidationStatus.INVALID
    assert len(validation.errors) == 2
    assert "Erro 1" in validation.errors
    assert "Erro 2" in validation.errors

def test_get_form_validation_pending(validation_summary, mock_state_manager):
    """Testa obtenção de validação para formulário pendente."""
    # Simula formulário não iniciado
    form_data = Mock(data={}, is_valid=False, state=FormState.INITIAL)
    mock_state_manager.get_form_data.return_value = form_data
    
    validation = validation_summary.get_form_validation("identification")
    
    assert validation.status == ValidationStatus.PENDING
    assert not validation.errors
    assert not validation.warnings

def test_get_all_validations(validation_summary):
    """Testa obtenção de todas as validações."""
    validations = validation_summary.get_all_validations()
    
    assert len(validations) == 9  # Total de formulários
    assert all(isinstance(v, FormValidation) for v in validations)

def test_render_summary(validation_summary, monkeypatch):
    """Testa renderização do resumo."""
    # Mock das funções do Streamlit
    mock_write = monkeypatch.setattr("streamlit.write", lambda *args: None)
    mock_progress = monkeypatch.setattr("streamlit.progress", lambda x: None)
    mock_caption = monkeypatch.setattr("streamlit.caption", lambda x: None)
    
    # Mock do expander
    expander = Mock()
    expander.__enter__ = Mock(return_value=expander)
    expander.__exit__ = Mock(return_value=None)
    mock_expander = monkeypatch.setattr(
        "streamlit.expander",
        lambda *args, **kwargs: expander
    )
    
    # Mock do button
    mock_button = monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: False
    )
    
    # Mock de error e warning
    mock_error = monkeypatch.setattr("streamlit.error", lambda *args: None)
    mock_warning = monkeypatch.setattr("streamlit.warning", lambda *args: None)
    
    validation_summary.render()
    
    # Verifica se o expander foi usado
    assert expander.__enter__.called
    assert expander.__exit__.called 