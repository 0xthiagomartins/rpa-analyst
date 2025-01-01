"""Testes para o StateManager."""
import pytest
from unittest.mock import MagicMock
from src.views.components.state.state_manager import StateManager, FormState, FormData

@pytest.fixture
def mock_session_state():
    """Mock para o session_state do Streamlit."""
    return {
        'form_states': {},
        'current_form': None,
        'navigation_history': []
    }

@pytest.fixture
def state_manager(monkeypatch, mock_session_state):
    """Fixture que retorna um StateManager configurado para testes."""
    monkeypatch.setattr("streamlit.session_state", mock_session_state)
    return StateManager()

def test_initialization(state_manager, mock_session_state):
    """Testa inicialização do StateManager."""
    assert 'form_states' in mock_session_state
    assert 'current_form' in mock_session_state
    assert 'navigation_history' in mock_session_state
    assert isinstance(mock_session_state['form_states'], dict)
    assert mock_session_state['navigation_history'] == []

def test_update_form_data(state_manager, mock_session_state):
    """Testa atualização de dados do formulário."""
    form_id = "test_form"
    data = {"field1": "value1"}
    
    state_manager.update_form_data(form_id, data)
    
    form_data = state_manager.get_form_data(form_id)
    assert form_data.data == data
    assert form_data.state == FormState.EDITING

def test_set_form_errors(state_manager):
    """Testa definição de erros do formulário."""
    form_id = "test_form"
    errors = {"field1": "Error message"}
    
    state_manager.set_form_errors(form_id, errors)
    
    form_data = state_manager.get_form_data(form_id)
    assert form_data.errors == errors
    assert form_data.state == FormState.ERROR
    assert not form_data.is_valid

def test_navigation(state_manager, mock_session_state):
    """Testa navegação entre formulários."""
    form1 = "form1"
    form2 = "form2"
    
    state_manager.navigate_to(form1)
    assert mock_session_state['current_form'] == form1
    
    state_manager.navigate_to(form2)
    assert mock_session_state['current_form'] == form2
    assert mock_session_state['navigation_history'] == [form1]

def test_go_back(state_manager):
    """Testa navegação de volta."""
    form1 = "form1"
    form2 = "form2"
    
    state_manager.navigate_to(form1)
    state_manager.navigate_to(form2)
    
    assert state_manager.can_go_back()
    previous = state_manager.go_back()
    assert previous == form1
    assert state_manager.get_current_form() == form1

def test_reset_form(state_manager):
    """Testa reset do formulário."""
    form_id = "test_form"
    data = {"field1": "value1"}
    
    state_manager.update_form_data(form_id, data)
    state_manager.reset_form(form_id)
    
    form_data = state_manager.get_form_data(form_id)
    assert form_data.data == {}
    assert form_data.state == FormState.INITIAL 