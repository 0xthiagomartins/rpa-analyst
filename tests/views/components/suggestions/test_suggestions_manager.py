"""Testes para o gerenciador de sugestões."""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import streamlit as st
from src.views.components.suggestions.suggestions_manager import SuggestionsManager
from src.services.ai_types import AIResponse

@pytest.fixture
def mock_session_state():
    """Mock do session_state do Streamlit."""
    class SessionState(dict):
        def __setattr__(self, name, value):
            self[name] = value
            
        def __getattr__(self, name):
            if name not in self:
                self[name] = {}
            return self[name]
    
    with patch("streamlit.session_state", SessionState()) as mock_state:
        yield mock_state

@pytest.fixture
def suggestions_manager():
    """Fixture que fornece uma instância do SuggestionsManager."""
    return SuggestionsManager()

@pytest.fixture
def mock_suggestions():
    """Mock de sugestões da IA."""
    return {
        "description": "Descrição melhorada do processo",
        "forms_data": {
            "identification": {
                "form_id": "identification",
                "is_valid": True,
                "has_changes": True,
                "data": {
                    "name": "Processo Teste",
                    "responsible": "Equipe Teste"
                }
            }
        },
        "suggestions": [
            "Sugestão 1",
            "Sugestão 2"
        ],
        "validation": [
            "Validação 1"
        ]
    }

@pytest.mark.asyncio
async def test_request_suggestions_success(
    suggestions_manager,
    mock_session_state,
    mock_suggestions
):
    """Testa solicitação de sugestões com sucesso."""
    with patch('src.services.ai_service.AIService.suggest_improvements', 
               new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = mock_suggestions
        
        await suggestions_manager.request_suggestions("descrição teste")
        
        assert mock_session_state.suggestions_buffer == mock_suggestions
        mock_ai.assert_called_once_with("descrição teste", None)

@pytest.mark.asyncio
async def test_request_suggestions_error(
    suggestions_manager,
    mock_session_state
):
    """Testa erro na solicitação de sugestões."""
    with patch('src.services.ai_service.AIService.suggest_improvements',
               side_effect=Exception("Erro teste")):
        with patch('streamlit.error') as mock_error:
            await suggestions_manager.request_suggestions("descrição teste")
            
            mock_error.assert_called_once()
            assert mock_session_state.suggestions_buffer is None

def test_render_preview_no_suggestions(
    suggestions_manager,
    mock_session_state
):
    """Testa renderização sem sugestões."""
    with patch('streamlit.write') as mock_write:
        suggestions_manager.render_preview()
        mock_write.assert_not_called()

def test_render_preview_with_suggestions(
    suggestions_manager,
    mock_session_state,
    mock_suggestions
):
    """Testa renderização com sugestões."""
    mock_session_state.suggestions_buffer = mock_suggestions
    
    with patch('streamlit.write') as mock_write:
        with patch('streamlit.expander') as mock_expander:
            suggestions_manager.render_preview()
            
            mock_write.assert_called()
            mock_expander.assert_called()

def test_apply_description(
    suggestions_manager,
    mock_session_state
):
    """Testa aplicação de descrição melhorada."""
    description = "Nova descrição"
    suggestions_manager._apply_description(description)
    
    assert mock_session_state.process_data["description"] == description

def test_apply_suggestions(
    suggestions_manager,
    mock_session_state,
    mock_suggestions
):
    """Testa aplicação de sugestões."""
    mock_session_state.suggestions_buffer = mock_suggestions
    selected_forms = ["identification"]
    
    suggestions_manager._apply_suggestions(selected_forms)
    
    assert mock_session_state.identification == {
        "name": "Processo Teste",
        "responsible": "Equipe Teste"
    }

def test_discard_suggestions(
    suggestions_manager,
    mock_session_state,
    mock_suggestions
):
    """Testa descarte de sugestões."""
    mock_session_state.suggestions_buffer = mock_suggestions
    
    suggestions_manager._discard_suggestions()
    
    assert mock_session_state.suggestions_buffer is None 