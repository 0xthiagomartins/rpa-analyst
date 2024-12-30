"""Testes para o orquestrador de formulários."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.process_form import ProcessForm
from src.utils.dependency_container import DependencyContainer
from src.controllers.process_controller import ProcessController

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.process_form.st") as mock_st:
        # Simula colunas
        col1, col2 = Mock(), Mock()
        mock_st.columns.return_value = [col1, col2]
        
        # Simula contexto das colunas
        col1.__enter__ = lambda x: col1
        col1.__exit__ = lambda x, y, z, w: None
        col2.__enter__ = lambda x: col2
        col2.__exit__ = lambda x, y, z, w: None
        
        yield mock_st

@pytest.fixture
def mock_container():
    """Mock para o container de dependências."""
    container = Mock(spec=DependencyContainer)
    controller = Mock(spec=ProcessController)
    validator = Mock()
    validator.validate_form.return_value = []
    
    # Configura o container para retornar o controller ou validator dependendo do tipo solicitado
    def resolve_side_effect(service_type):
        if service_type == ProcessController:
            return controller
        return validator
        
    container.resolve.side_effect = resolve_side_effect
    return container

def test_process_form_initialization(mock_container):
    """Testa inicialização do orquestrador."""
    form = ProcessForm(mock_container)
    assert form._current_step == 0
    assert len(form.forms) == 4
    assert form._data == {}

def test_next_step_with_valid_form(mock_container):
    """Testa avanço com formulário válido."""
    form = ProcessForm(mock_container)
    form.current_form.validate = Mock(return_value=True)
    
    assert form.next_step() == True
    assert form._current_step == 1

def test_next_step_with_invalid_form(mock_container):
    """Testa avanço com formulário inválido."""
    form = ProcessForm(mock_container)
    form.current_form.validate = Mock(return_value=False)
    
    assert form.next_step() == False
    assert form._current_step == 0

def test_previous_step(mock_container):
    """Testa retorno ao passo anterior."""
    form = ProcessForm(mock_container)
    form._current_step = 1
    
    assert form.previous_step() == True
    assert form._current_step == 0

def test_save_success(mock_container, mock_streamlit):
    """Testa salvamento com sucesso."""
    form = ProcessForm(mock_container)
    form.controller.create_process.return_value = True
    
    assert form.save() == True
    mock_streamlit.success.assert_called_once()

def test_save_failure(mock_container, mock_streamlit):
    """Testa falha no salvamento."""
    form = ProcessForm(mock_container)
    form.controller.create_process.return_value = False
    
    assert form.save() == False
    mock_streamlit.error.assert_called_once()

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = ProcessForm(mock_container)
    # Mock o validate para não falhar durante a renderização
    form.current_form.validate = Mock(return_value=True)
    form.render()
    
    mock_streamlit.progress.assert_called_once()
    mock_streamlit.write.assert_called()
    mock_streamlit.columns.assert_called_once() 