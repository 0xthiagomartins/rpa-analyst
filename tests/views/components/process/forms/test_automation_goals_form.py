"""Testes para o formulário de objetivos da automação."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.automation_goals_form import AutomationGoalsForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.automation_goals_form.st") as mock_st:
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
        mock_st.text_area.return_value = ""
        mock_st.text_input.return_value = ""
        mock_st.button.return_value = False
        
        yield mock_st

@pytest.fixture
def mock_container():
    """Mock para o container de dependências."""
    container = Mock(spec=DependencyContainer)
    validator = Mock()
    validator.validate_form.return_value = []
    container.resolve.return_value = validator
    return container

def test_automation_goals_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = AutomationGoalsForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_automation_goals_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = AutomationGoalsForm(mock_container)
    form._data = {
        "automation_goals": ["Objetivo 1"],
        "kpis": [{"metric": "Tempo", "target": "10min"}]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_automation_goals_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = AutomationGoalsForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_goal(mock_container, mock_streamlit):
    """Testa adição de objetivo."""
    form = AutomationGoalsForm(mock_container)
    mock_streamlit.text_area.return_value = "Novo Objetivo"
    mock_streamlit.button.return_value = True
    
    form._add_goal(form._data.setdefault("automation_goals", []))
    
    assert "Novo Objetivo" in form._data["automation_goals"]

def test_add_kpi(mock_container, mock_streamlit):
    """Testa adição de KPI."""
    form = AutomationGoalsForm(mock_container)
    mock_streamlit.text_input.side_effect = ["Tempo", "10min"]
    mock_streamlit.button.return_value = True
    
    form._add_kpi(form._data.setdefault("kpis", []))
    
    assert {"metric": "Tempo", "target": "10min"} in form._data["kpis"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = AutomationGoalsForm(mock_container)
    form._data = {
        "automation_goals": ["Objetivo 1"],
        "kpis": [{"metric": "Tempo", "target": "10min"}]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 🎯 Objetivos da Automação")
    mock_streamlit.write.assert_any_call("#### Objetivos")
    mock_streamlit.write.assert_any_call("#### KPIs") 