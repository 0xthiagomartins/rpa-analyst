"""Testes para o formulário de regras de negócio."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.business_rules_form import BusinessRulesForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.business_rules_form.st") as mock_st:
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

def test_business_rules_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = BusinessRulesForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_business_rules_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = BusinessRulesForm(mock_container)
    form._data = {
        "business_rules": ["Regra 1", "Regra 2"],
        "exceptions": ["Exceção 1"]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_business_rules_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = BusinessRulesForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_business_rule(mock_container, mock_streamlit):
    """Testa adição de regra de negócio."""
    form = BusinessRulesForm(mock_container)
    mock_streamlit.text_area.return_value = "Nova Regra"
    mock_streamlit.button.return_value = True
    
    form._add_rule(form._data.setdefault("business_rules", []))
    
    assert "Nova Regra" in form._data["business_rules"]

def test_add_exception(mock_container, mock_streamlit):
    """Testa adição de exceção."""
    form = BusinessRulesForm(mock_container)
    mock_streamlit.text_area.return_value = "Nova Exceção"
    mock_streamlit.button.return_value = True
    
    form._add_exception(form._data.setdefault("exceptions", []))
    
    assert "Nova Exceção" in form._data["exceptions"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = BusinessRulesForm(mock_container)
    form._data = {
        "business_rules": ["Regra 1"],
        "exceptions": ["Exceção 1"]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 📜 Regras de Negócio e Exceções")
    mock_streamlit.write.assert_any_call("#### Regras de Negócio")
    mock_streamlit.write.assert_any_call("#### Exceções") 