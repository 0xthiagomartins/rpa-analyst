"""Testes para o buffer de sugestões."""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from src.views.components.suggestions.suggestions_buffer import (
    SuggestionsBuffer,
    SuggestionData
)

@pytest.fixture
def mock_session_state():
    """Mock para o session_state do Streamlit."""
    class MockSessionState(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__dict__ = self
    return MockSessionState()

@pytest.fixture
def suggestions_buffer(monkeypatch, mock_session_state):
    """Fixture que fornece um buffer configurado para testes."""
    monkeypatch.setattr("streamlit.session_state", mock_session_state)
    return SuggestionsBuffer()

def test_initialization(suggestions_buffer, mock_session_state):
    """Testa inicialização do buffer."""
    assert 'suggestions_buffer' in st.session_state
    assert isinstance(st.session_state.suggestions_buffer, dict)

def test_add_suggestion(suggestions_buffer):
    """Testa adição de sugestão."""
    form_id = "test_form"
    data = {"field": "value"}
    
    suggestions_buffer.add_suggestion(form_id, data, confidence=0.8)
    
    suggestion = suggestions_buffer.get_suggestion(form_id)
    assert suggestion is not None
    assert suggestion.form_id == form_id
    assert suggestion.data == data
    assert suggestion.confidence == 0.8
    assert isinstance(suggestion.timestamp, datetime)
    assert not suggestion.applied

def test_mark_as_applied(suggestions_buffer):
    """Testa marcação de sugestão como aplicada."""
    form_id = "test_form"
    suggestions_buffer.add_suggestion(form_id, {"field": "value"})
    
    suggestions_buffer.mark_as_applied(form_id)
    
    suggestion = suggestions_buffer.get_suggestion(form_id)
    assert suggestion.applied

def test_clear_suggestions(suggestions_buffer):
    """Testa limpeza de sugestões."""
    suggestions_buffer.add_suggestion("form1", {"field": "value1"})
    suggestions_buffer.add_suggestion("form2", {"field": "value2"})
    
    suggestions_buffer.clear_suggestions()
    
    assert not suggestions_buffer.has_suggestions("form1")
    assert not suggestions_buffer.has_suggestions("form2")

def test_has_suggestions(suggestions_buffer):
    """Testa verificação de existência de sugestões."""
    form_id = "test_form"
    
    assert not suggestions_buffer.has_suggestions(form_id)
    
    suggestions_buffer.add_suggestion(form_id, {"field": "value"})
    assert suggestions_buffer.has_suggestions(form_id) 