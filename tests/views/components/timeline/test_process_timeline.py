"""Testes para o ProcessTimeline."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.timeline.process_timeline import (
    ProcessTimeline,
    TimelineStep,
    StepStatus
)

@pytest.fixture
def mock_state_manager():
    """Mock para o StateManager."""
    manager = Mock()
    manager.get_current_form.return_value = "identification"
    return manager

@pytest.fixture
def timeline(mock_state_manager):
    """Fixture que retorna um ProcessTimeline configurado para testes."""
    return ProcessTimeline(state_manager=mock_state_manager)

def test_initialization(timeline):
    """Testa inicialização do timeline."""
    assert len(timeline.steps) == 9  # Total de passos
    assert all(isinstance(step, TimelineStep) for step in timeline.steps)
    assert all(step.status == StepStatus.PENDING for step in timeline.steps)

def test_update_step_status(timeline):
    """Testa atualização de status do passo."""
    step_id = "identification"
    errors = ["Campo obrigatório"]
    
    timeline.update_step_status(step_id, StepStatus.ERROR, errors)
    
    step = next(s for s in timeline.steps if s.id == step_id)
    assert step.status == StepStatus.ERROR
    assert step.validation_errors == errors

def test_get_current_step(timeline, mock_state_manager):
    """Testa obtenção do passo atual."""
    current = timeline.get_current_step()
    
    assert current is not None
    assert current.id == "identification"
    mock_state_manager.get_current_form.assert_called_once()

def test_get_next_step(timeline):
    """Testa obtenção do próximo passo."""
    next_step = timeline.get_next_step()
    
    assert next_step is not None
    assert next_step.id == "details"
    assert next_step.order == 2

def test_get_previous_step(timeline):
    """Testa obtenção do passo anterior."""
    # Define um passo atual que não seja o primeiro
    timeline.state_manager.get_current_form.return_value = "details"
    
    prev_step = timeline.get_previous_step()
    
    assert prev_step is not None
    assert prev_step.id == "identification"
    assert prev_step.order == 1

def test_render_timeline(timeline, monkeypatch):
    """Testa renderização do timeline."""
    # Mock das funções do Streamlit
    mock_write = monkeypatch.setattr("streamlit.write", lambda *args: None)
    mock_progress = monkeypatch.setattr("streamlit.progress", lambda x: None)
    mock_caption = monkeypatch.setattr("streamlit.caption", lambda x: None)
    
    # Cria mocks para as colunas com suporte a context manager
    col1, col2 = Mock(), Mock()
    col1.__enter__ = Mock(return_value=col1)
    col1.__exit__ = Mock(return_value=None)
    col2.__enter__ = Mock(return_value=col2)
    col2.__exit__ = Mock(return_value=None)
    
    # Mock do st.columns que retorna as colunas preparadas
    mock_columns = monkeypatch.setattr(
        "streamlit.columns", 
        lambda *args: [col1, col2]
    )
    
    # Mock do st.expander
    expander = Mock()
    expander.__enter__ = Mock(return_value=expander)
    expander.__exit__ = Mock(return_value=None)
    mock_expander = monkeypatch.setattr(
        "streamlit.expander",
        lambda *args, **kwargs: expander
    )
    
    # Mock do st.button
    mock_button = monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: False
    )
    
    # Mock do st.error
    mock_error = monkeypatch.setattr(
        "streamlit.error",
        lambda *args: None
    )
    
    # Marca alguns passos como completos
    timeline.update_step_status("identification", StepStatus.COMPLETED)
    timeline.update_step_status("details", StepStatus.CURRENT)
    
    # Adiciona alguns erros para testar o expander
    timeline.update_step_status(
        "rules", 
        StepStatus.ERROR, 
        ["Erro de validação"]
    )
    
    timeline.render()
    
    # Verifica se os métodos foram chamados
    assert col1.__enter__.called
    assert col2.__enter__.called
    assert col1.__exit__.called
    assert col2.__exit__.called 