"""Testes para o formulário de identificação."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.identification_form import IdentificationForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.identification_form.st") as mock_st:
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
    validator = Mock()
    validator.validate_form.return_value = []
    container.resolve.return_value = validator
    return container

def test_identification_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = IdentificationForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_identification_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = IdentificationForm(mock_container)
    form._data = {
        "process_name": "Processo 1",
        "process_owner": "Responsável",
        "department": "Departamento",
        "current_status": "Em andamento",
        "estimated_time": "2 semanas"
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_identification_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = IdentificationForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = IdentificationForm(mock_container)
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 🎯 Identificação do Processo")
    # Verifica se os campos foram renderizados
    mock_streamlit.text_input.assert_any_call(
        "Nome do Processo",
        value="",
        help="Nome do processo a ser automatizado"
    ) 