"""Testes para o formulário de passos."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.steps_form import StepsForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.steps_form.st") as mock_st:
        # Simula colunas
        col1, col2 = Mock(), Mock()
        
        # Corrige o side_effect para aceitar tanto int quanto list
        def columns_side_effect(spec):
            if isinstance(spec, (int, list)):
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
        mock_st.number_input.return_value = 1
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

def test_steps_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = StepsForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_steps_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = StepsForm(mock_container)
    form._data = {
        "steps_as_is": [{
            "sequence": 1,
            "description": "Passo 1",
            "actor": "João",
            "system": "SAP"
        }],
        "steps_to_be": [{
            "sequence": 1,
            "description": "Passo 1 Automatizado",
            "actor": "Bot",
            "system": "SAP"
        }]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_steps_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = StepsForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_step_as_is(mock_container, mock_streamlit):
    """Testa adição de passo as-is."""
    form = StepsForm(mock_container)
    mock_streamlit.text_area.return_value = "Passo 1"
    mock_streamlit.number_input.return_value = 1
    mock_streamlit.text_input.side_effect = ["João", "SAP"]
    mock_streamlit.button.return_value = True
    
    form._add_step(form._data.setdefault("steps_as_is", []), "as_is")
    
    assert {
        "sequence": 1,
        "description": "Passo 1",
        "actor": "João",
        "system": "SAP"
    } in form._data["steps_as_is"]

def test_add_step_to_be(mock_container, mock_streamlit):
    """Testa adição de passo to-be."""
    form = StepsForm(mock_container)
    mock_streamlit.text_area.return_value = "Passo 1 Automatizado"
    mock_streamlit.number_input.return_value = 1
    mock_streamlit.text_input.side_effect = ["Bot", "SAP"]
    mock_streamlit.button.return_value = True
    
    form._add_step(form._data.setdefault("steps_to_be", []), "to_be")
    
    assert {
        "sequence": 1,
        "description": "Passo 1 Automatizado",
        "actor": "Bot",
        "system": "SAP"
    } in form._data["steps_to_be"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = StepsForm(mock_container)
    form._data = {
        "steps_as_is": [{
            "sequence": 1,
            "description": "Passo 1",
            "actor": "João",
            "system": "SAP"
        }],
        "steps_to_be": [{
            "sequence": 1,
            "description": "Passo 1 Automatizado",
            "actor": "Bot",
            "system": "SAP"
        }]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 👣 Passos do Processo")
    mock_streamlit.write.assert_any_call("#### Processo Atual (As-Is)")
    mock_streamlit.write.assert_any_call("#### Processo Futuro (To-Be)") 