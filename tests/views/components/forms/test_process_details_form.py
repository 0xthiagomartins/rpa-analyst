"""Testes para o formulário de detalhes do processo."""
import pytest
from unittest.mock import Mock, patch
import streamlit as st
from src.views.components.forms.process_details_form import ProcessDetailsForm
from src.views.components.state.suggestions_buffer import SuggestionsState, SuggestionBuffer
from datetime import datetime
from unittest.mock import AsyncMock

@pytest.fixture
def form():
    """Fixture que fornece uma instância do formulário."""
    return ProcessDetailsForm()

@pytest.fixture
def mock_session_state():
    """Fixture que fornece um mock do session_state."""
    class SessionState(dict):
        def __setattr__(self, name, value):
            self[name] = value
        def __getattr__(self, name):
            return self.get(name)
            
    with patch.object(st, 'session_state', SessionState()) as mock_state:
        yield mock_state

@pytest.fixture
def mock_streamlit():
    """Fixture que fornece mocks das funções do Streamlit."""
    with patch('streamlit.write') as mock_write, \
         patch('streamlit.text_area') as mock_text_area, \
         patch('streamlit.selectbox') as mock_select, \
         patch('streamlit.number_input') as mock_number, \
         patch('streamlit.error') as mock_error:
        yield {
            'write': mock_write,
            'text_area': mock_text_area,
            'selectbox': mock_select,
            'number_input': mock_number,
            'error': mock_error
        }

@pytest.mark.asyncio
async def test_render_basic(form, mock_streamlit, mock_session_state):
    """Testa renderização básica do formulário."""
    await form.render()
    
    mock_streamlit['write'].assert_called_with("### 📋 Detalhes do Processo")
    assert mock_streamlit['text_area'].call_count == 3
    assert mock_streamlit['selectbox'].call_count == 1
    assert mock_streamlit['number_input'].call_count == 2

@pytest.mark.asyncio
async def test_render_with_suggestions(form, mock_streamlit, mock_session_state):
    """Testa renderização com sugestões disponíveis."""
    # Mock do render_suggestions
    form.render_suggestions = AsyncMock()
    
    # Configura buffer de sugestões
    buffer = SuggestionBuffer(
        timestamp=datetime.now(),
        description="Teste",
        forms_data={
            "process_details": {
                "data": {
                    "process_objective": "Objetivo sugerido",
                    "process_scope": "Escopo sugerido"
                }
            }
        },
        suggestions=["Sugestão 1"],
        validation=["Validação 1"]
    )
    SuggestionsState.set_buffer(buffer)
    
    # Mock do rerun para evitar interrupção
    with patch('streamlit.rerun', side_effect=lambda: None):
        await form.render()
    
    # Verifica se preview foi renderizado
    assert mock_streamlit['write'].call_count >= 1

@pytest.mark.asyncio
async def test_render_with_existing_data(form, mock_streamlit, mock_session_state):
    """Testa renderização com dados existentes."""
    # Configura dados existentes
    mock_session_state.update({
        'process_objective': "Objetivo existente",
        'process_scope': "Escopo existente",
        'frequency': "Semanal",
        'monthly_volume': 100,
        'time_per_execution': 30,
        'data_used': "Dados existentes"
    })
    
    await form.render()
    
    # Verifica se campos foram preenchidos com dados existentes
    calls = mock_streamlit['text_area'].call_args_list
    assert calls[0][1]['value'] == "Objetivo existente"
    assert calls[1][1]['value'] == "Escopo existente" 