"""Testes para o formulário de dados."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.data_form import DataForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.data_form.st") as mock_st:
        # Simula colunas
        col1, col2 = Mock(), Mock()
        
        # Corrige o side_effect para aceitar tanto int quanto list
        def columns_side_effect(spec):
            if isinstance(spec, int):
                return [col1, col2]
            return [col1, col2]
            
        mock_st.columns.side_effect = columns_side_effect
        
        # Simula contexto das colunas
        for col in [col1, col2]:
            col.__enter__ = lambda x: col
            col.__exit__ = lambda x, y, z, w: None
        
        # Configura retornos padrão
        mock_st.text_input.return_value = ""
        mock_st.text_area.return_value = ""
        mock_st.selectbox.return_value = "Texto"
        mock_st.button.return_value = False
        mock_st.expander.return_value.__enter__ = lambda x: mock_st
        mock_st.expander.return_value.__exit__ = lambda x, y, z, w: None
        
        yield mock_st

@pytest.fixture
def mock_container():
    """Mock para o container de dependências."""
    container = Mock(spec=DependencyContainer)
    validator = Mock()
    validator.validate_form.return_value = []
    container.resolve.return_value = validator
    return container

def test_data_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = DataForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_data_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = DataForm(mock_container)
    form._data = {
        "inputs": [{"name": "CPF", "type": "Texto", "description": "CPF do cliente"}],
        "outputs": [{"name": "Status", "type": "Texto", "description": "Status do processo"}]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_data_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = DataForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_input(mock_container, mock_streamlit):
    """Testa adição de entrada."""
    form = DataForm(mock_container)
    mock_streamlit.text_input.return_value = "CPF"
    mock_streamlit.selectbox.return_value = "Texto"
    mock_streamlit.text_area.return_value = "CPF do cliente"
    mock_streamlit.button.return_value = True
    
    form._add_input(form._data.setdefault("inputs", []))
    
    assert {
        "name": "CPF",
        "type": "Texto",
        "description": "CPF do cliente"
    } in form._data["inputs"]

def test_add_output(mock_container, mock_streamlit):
    """Testa adição de saída."""
    form = DataForm(mock_container)
    mock_streamlit.text_input.return_value = "Status"
    mock_streamlit.selectbox.return_value = "Texto"
    mock_streamlit.text_area.return_value = "Status do processo"
    mock_streamlit.button.return_value = True
    
    form._add_output(form._data.setdefault("outputs", []))
    
    assert {
        "name": "Status",
        "type": "Texto",
        "description": "Status do processo"
    } in form._data["outputs"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = DataForm(mock_container)
    form._data = {
        "inputs": [{"name": "CPF", "type": "Texto", "description": "CPF do cliente"}],
        "outputs": [{"name": "Status", "type": "Texto", "description": "Status do processo"}]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 📊 Dados do Processo")
    mock_streamlit.write.assert_any_call("#### Dados de Entrada")
    mock_streamlit.write.assert_any_call("#### Dados de Saída") 