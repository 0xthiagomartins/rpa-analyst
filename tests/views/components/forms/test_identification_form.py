"""Testes para o formulário de identificação."""
import pytest
from unittest.mock import Mock, patch
import streamlit as st
from src.views.components.forms.identification_form import IdentificationForm
from src.views.components.state.suggestions_buffer import SuggestionsState, SuggestionBuffer
from datetime import datetime

@pytest.fixture
def identification_form():
    """Fixture que fornece uma instância do IdentificationForm."""
    return IdentificationForm()  # Removido api_key pois não é mais necessário

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
         patch('streamlit.text_input') as mock_text_input, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.columns') as mock_columns, \
         patch('streamlit.error') as mock_error:
        yield {
            'write': mock_write,
            'text_area': mock_text_area,
            'text_input': mock_text_input,
            'button': mock_button,
            'columns': mock_columns,
            'error': mock_error
        }

@pytest.mark.asyncio  # Marca o teste como assíncrono
async def test_render_basic_form(identification_form, mock_streamlit, mock_session_state):
    """Testa renderização básica do formulário."""
    await identification_form.render()
    
    # Verifica se o título foi chamado (pode ser chamado mais de uma vez)
    mock_streamlit['write'].assert_any_call("### 🎯 Identificação do Processo")
    assert mock_streamlit['text_input'].call_count == 3
    assert mock_streamlit['text_area'].call_count == 1

@pytest.mark.asyncio
async def test_render_with_suggestions(identification_form, mock_streamlit, mock_session_state):
    """Testa renderização com sugestões disponíveis."""
    # Configura buffer de sugestões
    buffer = SuggestionBuffer(
        timestamp=datetime.now(),
        description="Teste",
        forms_data={
            "identification": {
                "data": {
                    "process_name": "Nome sugerido",
                    "responsible": "Responsável sugerido"
                }
            }
        },
        suggestions=["Sugestão 1"],
        validation=["Validação 1"]
    )
    SuggestionsState.set_buffer(buffer)
    
    await identification_form.render()
    
    # Verifica se preview foi renderizado
    assert mock_streamlit['write'].call_count > 1

@pytest.mark.asyncio
async def test_render_suggestion_error(identification_form, mock_streamlit, mock_session_state):
    """Testa erro ao gerar sugestões."""
    mock_session_state.update({
        'description': "Descrição teste",
        'requesting_suggestions': True
    })
    
    await identification_form.render()
    
    # Verifica se erro foi mostrado
    mock_streamlit['error'].assert_called_once()

@pytest.mark.asyncio
async def test_render_with_existing_data(identification_form, mock_streamlit, mock_session_state):
    """Testa renderização com dados existentes."""
    # Configura dados existentes
    mock_session_state.update({
        'process_name': "Nome existente",
        'responsible': "Responsável existente",
        'area': "Área existente",
        'description': "Descrição existente"
    })
    
    await identification_form.render()
    
    # Verifica se campos foram preenchidos com dados existentes
    calls = mock_streamlit['text_input'].call_args_list
    assert calls[0][1]['value'] == "Nome existente"
    assert calls[1][1]['value'] == "Responsável existente"
    assert calls[2][1]['value'] == "Área existente" 