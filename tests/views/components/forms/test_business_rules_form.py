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
    # Mock do render_suggestions
    form.render_suggestions = AsyncMock()
    
    # Configura dados existentes
    initial_rules = ["Regra 1", "Regra 2"]
    initial_exceptions = ["Exceção 1"]
    
    # Mock para controlar a ordem das chamadas
    text_area_values = []
    text_area_keys = []
    
    def mock_text_area(*args, **kwargs):
        print(f"mock_text_area chamado com args={args}, kwargs={kwargs}")  # Debug
        key = kwargs.get('key', '')
        value = ''
        
        if key.startswith('rule_'):
            index = int(key.split('_')[1])
            value = initial_rules[index] if index < len(initial_rules) else ''
        elif key.startswith('exception_'):
            index = int(key.split('_')[1])
            value = initial_exceptions[index] if index < len(initial_exceptions) else ''
        
        text_area_values.append(value)
        text_area_keys.append(key)
        return value
    
    # Substitui o mock original
    mock_streamlit['text_area'].side_effect = mock_text_area
    
    # Configura dados iniciais
    mock_session_state.update({
        'business_rules': initial_rules.copy(),
        'exceptions': initial_exceptions.copy()
    })
    
    # Mock para simular o contexto das colunas
    class MockColumn:
        def __init__(self, name):
            self.name = name
            self.text_area = mock_text_area  # Adiciona referência ao text_area
            
        def __enter__(self):
            print(f"Entrando na coluna {self.name}")
            return self
            
        def __exit__(self, *args):
            print(f"Saindo da coluna {self.name}")
            
        def text_area(self, *args, **kwargs):
            # Delega para o mock_text_area
            return mock_text_area(*args, **kwargs)

    def mock_columns(*args):
        print(f"mock_columns chamado com args={args}")  # Debug
        col1, col2 = MockColumn("col1"), MockColumn("col2")
        return [col1, col2]

    # Cria um módulo mock para o streamlit
    mock_streamlit_module = MagicMock()
    mock_streamlit_module.session_state = mock_session_state
    mock_streamlit_module.write = mock_streamlit['write']
    mock_streamlit_module.text_area = mock_text_area
    mock_streamlit_module.button = mock_streamlit['button']
    mock_streamlit_module.columns = mock_columns
    mock_streamlit_module.error = mock_streamlit['error']
    
    # Aplica o patch do módulo streamlit
    with patch.dict('sys.modules', {'streamlit': mock_streamlit_module}):
        # Debug: imprime o estado antes do render
        print("Estado antes do render:", mock_session_state)
        print("Rules antes:", mock_session_state.get("business_rules"))
        
        # Executa o render
        await form.render()
        
        # Debug: imprime o estado depois do render
        print("Estado depois do render:", mock_session_state)
        print("Rules depois:", mock_session_state.get("business_rules"))
        print("Text area keys:", text_area_keys)  # Debug
        print("Text area values:", text_area_values)  # Debug
        
        # Verifica se todas as chaves esperadas estão presentes
        expected_keys = ['rule_0', 'rule_1', 'exception_0']
        for key in expected_keys:
            with check:
                assert key in text_area_keys, f"Chave {key} não encontrada em {text_area_keys}"
        
        # Verifica os valores
        with check:
            assert text_area_values == ["Regra 1", "Regra 2", "Exceção 1"]

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