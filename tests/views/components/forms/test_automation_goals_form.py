"""Testes para o formulário de objetivos da automação."""
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import streamlit as st
from pytest_check import check
from src.views.components.forms.automation_goals_form import AutomationGoalsForm
from src.views.components.state.suggestions_buffer import SuggestionsState, SuggestionBuffer
from datetime import datetime
from contextlib import ExitStack

@pytest.fixture
def form():
    """Fixture que fornece uma instância do formulário."""
    return AutomationGoalsForm()

@pytest.fixture
def mock_session_state():
    """Fixture que fornece um mock do session_state."""
    class MockSessionState:
        """Mock do session_state do Streamlit."""
        def __init__(self):
            self._data = {}
            
        def get(self, key, default=None):
            """Retorna valor do store com fallback para default."""
            value = self._data.get(key, default)
            if isinstance(value, list):
                return value.copy()
            return value
            
        def update(self, data):
            """Atualiza múltiplos valores no store."""
            for key, value in data.items():
                if isinstance(value, list):
                    self._data[key] = value.copy()
                else:
                    self._data[key] = value
                    
        def __getitem__(self, key):
            """Permite acesso via []."""
            return self.get(key)
            
        def __setitem__(self, key, value):
            """Permite atribuição via []."""
            if isinstance(value, list):
                self._data[key] = value.copy()
            else:
                self._data[key] = value
                
        def __getattr__(self, name):
            """Permite acesso via .atributo."""
            return self.get(name)
            
        def __str__(self):
            return str(self._data)
            
        def __repr__(self):
            return repr(self._data)
            
        def __contains__(self, key):
            """Permite uso do operador 'in'."""
            return key in self._data
    
    return MockSessionState()

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
    
    with patch.object(st, 'session_state', mock_session_state):
        await form.render()
    
    mock_streamlit['write'].assert_any_call("### 🎯 Objetivos da Automação")
    mock_streamlit['write'].assert_any_call("#### Objetivos Principais")
    mock_streamlit['write'].assert_any_call("#### Métricas de Sucesso")
    assert mock_streamlit['button'].call_count >= 2  # Botões de adicionar

@pytest.mark.asyncio
async def test_render_with_existing_data(form, mock_streamlit, mock_session_state):
    """Testa renderização com dados existentes."""
    # Mock do render_suggestions
    form.render_suggestions = AsyncMock()
    
    # Configura dados existentes
    initial_goals = ["Objetivo 1", "Objetivo 2"]
    initial_metrics = ["Métrica 1"]
    
    # Mock para controlar a ordem das chamadas
    text_area_values = []
    text_area_keys = []
    
    def mock_text_area(*args, **kwargs):
        print(f"mock_text_area chamado com args={args}, kwargs={kwargs}")
        key = kwargs.get('key', '')
        value = kwargs.get('value', '')
        
        text_area_values.append(value)
        text_area_keys.append(key)
        return value
    
    # Configura dados iniciais
    mock_session_state.update({
        'automation_goals': initial_goals.copy(),
        'success_metrics': initial_metrics.copy()
    })
    
    # Cria um módulo mock para o streamlit
    mock_streamlit_module = MagicMock()
    mock_streamlit_module.session_state = mock_session_state
    mock_streamlit_module.write = mock_streamlit['write']
    
    # Mock das colunas que retorna objetos com context manager
    def mock_columns(*args):
        print(f"mock_columns chamado com args={args}")
        return [MockColumn("col1", mock_text_area), MockColumn("col2", mock_text_area)]
    
    mock_streamlit_module.columns = mock_columns
    mock_streamlit_module.text_area = mock_text_area
    mock_streamlit_module.button = mock_streamlit['button']
    mock_streamlit_module.error = mock_streamlit['error']
    
    # Aplica o patch do módulo streamlit
    with patch.dict('sys.modules', {'streamlit': mock_streamlit_module}):
        # Debug: imprime o estado antes do render
        print("Estado antes do render:", mock_session_state)
        print("Goals antes:", mock_session_state.get("automation_goals"))
        
        # Executa o render
        await form.render()
        
        # Debug: imprime o estado depois do render
        print("Estado depois do render:", mock_session_state)
        print("Goals depois:", mock_session_state.get("automation_goals"))
        print("Text area keys:", text_area_keys)  # Debug
        print("Text area values:", text_area_values)  # Debug
        
        # Verifica se todas as chaves esperadas estão presentes
        expected_keys = ['goal_0', 'goal_1', 'metric_0']
        for key in expected_keys:
            with check:
                assert key in text_area_keys, f"Chave {key} não encontrada em {text_area_keys}"
        
        # Verifica os valores
        with check:
            assert text_area_values == ["Objetivo 1", "Objetivo 2", "Métrica 1"]

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
            "automation_goals": {
                "data": {
                    "automation_goals": ["Objetivo Sugerido"],
                    "success_metrics": ["Métrica Sugerida"]
                }
            }
        },
        suggestions=["Sugestão 1"],
        validation=["Validação 1"]
    )
    
    # Configura estado inicial e aplica sugestões
    mock_session_state.update({
        'automation_goals': [],
        'success_metrics': []
    })
    
    # Cria um módulo mock para o streamlit
    mock_streamlit_module = MagicMock()
    mock_streamlit_module.session_state = mock_session_state
    
    # Aplica os patches necessários
    patches = [
        patch('streamlit.session_state', new=mock_session_state),
        patch('streamlit.runtime.scriptrunner.get_script_run_ctx', return_value=True),
        patch('streamlit.rerun', side_effect=lambda: None),
        patch.dict('sys.modules', {'streamlit': mock_streamlit_module})
    ]
    
    # Executa com todos os patches ativos
    with ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
            
        SuggestionsState.set_buffer(buffer)
        form.apply_suggestions(buffer.forms_data["automation_goals"]["data"])
        
        # Verifica se as sugestões foram aplicadas corretamente
        with check:
            assert mock_session_state['automation_goals'] == ["Objetivo Sugerido"]
        with check:
            assert mock_session_state['success_metrics'] == ["Métrica Sugerida"] 