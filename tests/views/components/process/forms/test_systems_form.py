"""Testes para o formulário de sistemas."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.systems_form import SystemsForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.systems_form.st") as mock_st:
        # Simula colunas
        col1, col2, col3 = Mock(), Mock(), Mock()
        
        # Corrige o side_effect para aceitar tanto int quanto list
        def columns_side_effect(spec):
            if isinstance(spec, int):
                return [col1, col2] if spec == 2 else [col1, col2, col3]
            return [col1, col2] if len(spec) == 2 else [col1, col2, col3]
            
        mock_st.columns.side_effect = columns_side_effect
        
        # Simula contexto das colunas
        for col in [col1, col2, col3]:
            col.__enter__ = lambda x: col
            col.__exit__ = lambda x, y, z, w: None
        
        # Configura retornos padrão
        mock_st.text_input.return_value = ""
        mock_st.text_area.return_value = ""
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

def test_systems_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = SystemsForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_systems_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = SystemsForm(mock_container)
    form._data = {
        "systems": [{"name": "SAP", "role": "ERP"}],
        "integrations": [{"source": "SAP", "target": "Excel", "description": "Export"}]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_systems_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = SystemsForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_system(mock_container, mock_streamlit):
    """Testa adição de sistema."""
    form = SystemsForm(mock_container)
    mock_streamlit.text_input.side_effect = ["SAP", "ERP"]
    mock_streamlit.button.return_value = True
    
    form._add_system(form._data.setdefault("systems", []))
    
    assert {"name": "SAP", "role": "ERP"} in form._data["systems"]

def test_add_integration(mock_container, mock_streamlit):
    """Testa adição de integração."""
    form = SystemsForm(mock_container)
    mock_streamlit.text_input.side_effect = ["SAP", "Excel"]
    mock_streamlit.text_area.return_value = "Export data"
    mock_streamlit.button.return_value = True
    
    form._add_integration(form._data.setdefault("integrations", []))
    
    assert {
        "source": "SAP",
        "target": "Excel",
        "description": "Export data"
    } in form._data["integrations"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = SystemsForm(mock_container)
    form._data = {
        "systems": [{"name": "SAP", "role": "ERP"}],
        "integrations": [{"source": "SAP", "target": "Excel", "description": "Export"}]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 💻 Sistemas e Integrações")
    mock_streamlit.write.assert_any_call("#### Sistemas")
    mock_streamlit.write.assert_any_call("#### Integrações") 