"""Testes para o ErrorHandler."""
import pytest
from src.views.components.error.error_handler import ErrorHandler, ErrorLevel, ErrorMessage

@pytest.fixture
def mock_session_state():
    """Mock para o session_state do Streamlit."""
    return {'errors': []}

@pytest.fixture
def error_handler(monkeypatch, mock_session_state):
    """Fixture que retorna um ErrorHandler configurado para testes."""
    monkeypatch.setattr("streamlit.session_state", mock_session_state)
    return ErrorHandler()

def test_initialization(error_handler, mock_session_state):
    """Testa inicialização do ErrorHandler."""
    assert 'errors' in mock_session_state
    assert isinstance(mock_session_state['errors'], list)
    assert len(mock_session_state['errors']) == 0

def test_add_error(error_handler, mock_session_state):
    """Testa adição de erro."""
    error_handler.add_error(
        message="Erro de teste",
        level=ErrorLevel.ERROR,
        field="campo_teste",
        details={"info": "detalhes"}
    )
    
    assert len(mock_session_state['errors']) == 1
    error = mock_session_state['errors'][0]
    assert error.message == "Erro de teste"
    assert error.level == ErrorLevel.ERROR
    assert error.field == "campo_teste"
    assert error.details == {"info": "detalhes"}

def test_get_errors_by_level(error_handler):
    """Testa obtenção de erros por nível."""
    error_handler.add_error("Erro 1", ErrorLevel.ERROR)
    error_handler.add_error("Aviso 1", ErrorLevel.WARNING)
    error_handler.add_error("Erro 2", ErrorLevel.ERROR)
    
    errors = error_handler.get_errors(ErrorLevel.ERROR)
    assert len(errors) == 2
    assert all(e.level == ErrorLevel.ERROR for e in errors)
    
    warnings = error_handler.get_errors(ErrorLevel.WARNING)
    assert len(warnings) == 1
    assert warnings[0].level == ErrorLevel.WARNING

def test_clear_errors(error_handler):
    """Testa limpeza de erros."""
    error_handler.add_error("Erro 1", ErrorLevel.ERROR)
    error_handler.add_error("Aviso 1", ErrorLevel.WARNING)
    
    error_handler.clear_errors(ErrorLevel.ERROR)
    assert len(error_handler.get_errors(ErrorLevel.ERROR)) == 0
    assert len(error_handler.get_errors(ErrorLevel.WARNING)) == 1
    
    error_handler.clear_errors()
    assert len(error_handler.get_errors()) == 0

def test_has_errors(error_handler):
    """Testa verificação de existência de erros."""
    assert not error_handler.has_errors()
    
    error_handler.add_error("Erro 1", ErrorLevel.ERROR)
    assert error_handler.has_errors()
    assert error_handler.has_errors(ErrorLevel.ERROR)
    assert not error_handler.has_errors(ErrorLevel.WARNING)

def test_render_errors(error_handler, monkeypatch):
    """Testa renderização de erros."""
    # Mock das funções de renderização do Streamlit
    mock_info = monkeypatch.setattr("streamlit.info", lambda x: None)
    mock_warning = monkeypatch.setattr("streamlit.warning", lambda x: None)
    mock_error = monkeypatch.setattr("streamlit.error", lambda x: None)
    
    error_handler.add_error("Info", ErrorLevel.INFO)
    error_handler.add_error("Warning", ErrorLevel.WARNING)
    error_handler.add_error("Error", ErrorLevel.ERROR)
    error_handler.add_error("Critical", ErrorLevel.CRITICAL)
    
    error_handler.render_errors() 