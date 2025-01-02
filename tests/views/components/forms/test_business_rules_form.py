"""Testes para o formulário de regras de negócio."""
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import streamlit as st
from pytest_check import check
from src.views.components.forms.business_rules_form import BusinessRulesForm
from src.views.components.state.suggestions_buffer import SuggestionsState, SuggestionBuffer
from datetime import datetime
from contextlib import ExitStack

@pytest.fixture
def form():
    """Fixture que fornece uma instância do formulário."""
    return BusinessRulesForm()

@pytest.fixture
def mock_session_state():
    """Fixture que fornece um mock do session_state."""
    class SessionState(dict):
        def __init__(self, *args, **kwargs):
            self.store = {}
            super().__init__(*args, **kwargs)
            
        def __setattr__(self, name, value):
            if name == 'store':
                super().__setattr__(name, value)
            else:
                self.store[name] = value
                
        def __getattr__(self, name):
            return self.store.get(name)
            
        def get(self, key, default=None):
            return self.store.get(key, default)
            
        def update(self, other):
            self.store.update({k: v.copy() if isinstance(v, list) else v for k, v in other.items()})
            
        def __getitem__(self, key):
            return self.store.get(key, [])
            
        def __setitem__(self, key, value):
            self.store[key] = value.copy() if isinstance(value, list) else value  # Faz cópia de listas
            
    return SessionState()

@pytest.fixture
def mock_streamlit():
    """Fixture que fornece mocks das funções do Streamlit."""
    # Mock para retornar duas colunas
    mock_col1, mock_col2 = MagicMock(), MagicMock()
    mock_columns = MagicMock(return_value=[mock_col1, mock_col2])
    
    with patch('streamlit.write') as mock_write, \
         patch('streamlit.text_area') as mock_text_area, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.columns', mock_columns) as mock_cols, \
         patch('streamlit.error') as mock_error:
        yield {
            'write': mock_write,
            'text_area': mock_text_area,
            'button': mock_button,
            'columns': mock_cols,
            'error': mock_error,
            'col1': mock_col1,
            'col2': mock_col2
        }

@pytest.mark.asyncio
async def test_render_basic(form, mock_streamlit, mock_session_state):
    """Testa renderização básica do formulário."""
    # Mock do render_suggestions
    form.render_suggestions = AsyncMock()
    
    await form.render()
    
    mock_streamlit['write'].assert_any_call("### 📜 Regras de Negócio")
    mock_streamlit['write'].assert_any_call("#### Regras de Negócio")
    mock_streamlit['write'].assert_any_call("#### Exceções")
    assert mock_streamlit['button'].call_count >= 2  # Botões de adicionar

@pytest.mark.asyncio
async def test_render_with_existing_data(form, mock_streamlit, mock_session_state):
    """Testa renderização com dados existentes."""
    # Mock do render_suggestions para evitar chamadas assíncronas
    form.render_suggestions = AsyncMock()
    
    # Configura dados existentes
    mock_session_state.update({
        'business_rules': ["Regra existente"],
        'exceptions': ["Exceção existente"],
        'business_rules_list': [
            {"rule": "Regra existente", "type": "Validação"}
        ],
        'exceptions_list': [
            {"description": "Exceção existente", "handling": "Manual"}
        ]
    })
    
    # Aplica patch no session_state do Streamlit
    with patch('streamlit.session_state', mock_session_state):
        await form.render()
    
        # Verifica se campos foram preenchidos com dados existentes
        text_area_calls = mock_streamlit['text_area'].call_args_list
        
        # Verifica regras
        assert any(
            call[1].get('value') == "Regra existente" 
            for call in text_area_calls
        ), "Regra não encontrada nos campos"
        
        # Verifica exceções
        assert any(
            call[1].get('value') == "Exceção existente"
            for call in text_area_calls
        ), "Exceção não encontrada nos campos"

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
            "business_rules": {
                "data": {
                    "business_rules": ["Regra Sugerida"],
                    "exceptions": ["Exceção Sugerida"]
                }
            }
        },
        suggestions=["Sugestão 1"],
        validation=["Validação 1"]
    )
    
    # Configura estado inicial e aplica sugestões
    with patch.object(st, 'session_state', mock_session_state):
        mock_session_state.store.update({
            'business_rules': [],
            'exceptions': []
        })
        
        SuggestionsState.set_buffer(buffer)
        
        # Simula aplicação das sugestões
        form.apply_suggestions(buffer.forms_data["business_rules"]["data"])
        
        # Verifica se as sugestões foram aplicadas corretamente
        with check:
            assert mock_session_state['business_rules'] == ["Regra Sugerida"]
        with check:
            assert mock_session_state['exceptions'] == ["Exceção Sugerida"] 