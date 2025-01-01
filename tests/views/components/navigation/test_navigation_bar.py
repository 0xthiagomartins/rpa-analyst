"""Testes para o NavigationBar."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.navigation.navigation_bar import (
    NavigationBar,
    NavItem
)
from src.views.components.state.state_manager import FormState

@pytest.fixture
def mock_state_manager():
    """Mock para o StateManager."""
    manager = Mock()
    manager.get_current_form.return_value = "identification"
    
    # Simula um formulário válido
    form_data = Mock(
        data={"field": "value"},
        is_valid=True,
        state=FormState.COMPLETED
    )
    manager.get_form_data.return_value = form_data
    
    return manager

@pytest.fixture
def mock_error_handler():
    """Mock para o ErrorHandler."""
    handler = Mock()
    handler.get_errors.return_value = []
    return handler

@pytest.fixture
def navigation_bar(mock_state_manager, mock_error_handler):
    """Fixture que retorna um NavigationBar configurado para testes."""
    return NavigationBar(
        state_manager=mock_state_manager,
        error_handler=mock_error_handler
    )

def test_initialization(navigation_bar):
    """Testa inicialização da barra de navegação."""
    assert len(navigation_bar.nav_items) == 9  # Total de itens
    assert all(isinstance(item, NavItem) for item in navigation_bar.nav_items)

def test_update_nav_states(navigation_bar, mock_state_manager):
    """Testa atualização de estados dos itens."""
    navigation_bar._update_nav_states()
    
    # Verifica item ativo
    active_item = next(i for i in navigation_bar.nav_items if i.is_active)
    assert active_item.id == "identification"
    
    # Verifica que foi chamado get_form_data para cada item
    assert mock_state_manager.get_form_data.call_count == len(navigation_bar.nav_items)

def test_render_progress_bar(navigation_bar, monkeypatch):
    """Testa renderização da barra de progresso."""
    mock_progress = monkeypatch.setattr("streamlit.progress", lambda x: None)
    mock_caption = monkeypatch.setattr("streamlit.caption", lambda x: None)
    
    # Marca alguns itens como completos
    navigation_bar.nav_items[0].is_completed = True
    navigation_bar.nav_items[1].is_completed = True
    
    navigation_bar.render_progress_bar()

def test_render_breadcrumbs(navigation_bar, monkeypatch):
    """Testa renderização dos breadcrumbs."""
    mock_write = monkeypatch.setattr("streamlit.write", lambda x: None)
    
    navigation_bar._update_nav_states()
    navigation_bar.render_breadcrumbs()

def test_render_tabs(navigation_bar, monkeypatch):
    """Testa renderização das tabs."""
    # Mock das funções do Streamlit
    tabs = [Mock(), Mock(), Mock()]
    for tab in tabs:
        tab.__enter__ = Mock(return_value=tab)
        tab.__exit__ = Mock(return_value=None)
    
    mock_tabs = monkeypatch.setattr(
        "streamlit.tabs",
        lambda *args: tabs[:len(navigation_bar.nav_items)]
    )
    
    mock_info = monkeypatch.setattr("streamlit.info", lambda x: None)
    mock_error = monkeypatch.setattr("streamlit.error", lambda x: None)
    mock_success = monkeypatch.setattr("streamlit.success", lambda x: None)
    mock_warning = monkeypatch.setattr("streamlit.warning", lambda x: None)
    mock_button = monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: False
    )
    
    navigation_bar.render_tabs()

def test_render_sidebar(navigation_bar, monkeypatch):
    """Testa renderização da sidebar."""
    mock_sidebar = Mock()
    mock_sidebar.button = Mock(return_value=False)
    mock_sidebar.write = Mock()
    
    monkeypatch.setattr("streamlit.sidebar", mock_sidebar)
    
    navigation_bar.render_sidebar()
    
    # Verifica que foram criados botões para cada item
    assert mock_sidebar.button.call_count == len(navigation_bar.nav_items)

def test_render_invalid_style(navigation_bar):
    """Testa renderização com estilo inválido."""
    with pytest.raises(ValueError):
        navigation_bar.render(style="invalid") 