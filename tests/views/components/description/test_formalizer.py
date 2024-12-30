"""Testes para o formalizador de descrições."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.description.formalizer import DescriptionFormalizer
from src.services.ai_service import AIService
from src.utils.dependency_container import DependencyContainer
from src.utils.config_constants import UI_CONFIG
from unittest.mock import call

@pytest.fixture
def mock_streamlit():
    """Fixture para simular o Streamlit."""
    with patch('src.views.components.description.formalizer.st') as mock_st:
        # Simula as colunas
        col1, col2 = Mock(), Mock()
        mock_st.columns.return_value = [col1, col2]
        
        # Simula o contexto das colunas
        col1.__enter__ = lambda x: col1
        col1.__exit__ = lambda x, y, z, w: None
        col2.__enter__ = lambda x: col2
        col2.__exit__ = lambda x, y, z, w: None
        
        # Simula os componentes
        mock_st.text_area.return_value = "Texto original"
        mock_st.toggle.return_value = True
        mock_st.button.return_value = False
        
        yield mock_st

@pytest.fixture
def mock_container():
    """Fixture para simular o container."""
    container = Mock(spec=DependencyContainer)
    ai_service = Mock(spec=AIService)
    ai_service.formalize_description.return_value = "Texto formalizado"
    container.resolve.return_value = ai_service
    return container

def test_description_formalizer_initialization():
    """Testa a inicialização do formalizador."""
    formalizer = DescriptionFormalizer()
    assert formalizer._original_text == ""
    assert formalizer._formalized_text == ""
    assert formalizer._preview_enabled == True

def test_description_formalizer_with_custom_ai_service(mock_container):
    """Testa inicialização com serviço AI customizado."""
    formalizer = DescriptionFormalizer(container=mock_container)
    assert formalizer.container == mock_container
    assert isinstance(formalizer.ai_service, Mock)

def test_formalize_empty_text():
    """Testa formalização com texto vazio."""
    formalizer = DescriptionFormalizer()
    assert formalizer.formalize("") == False
    assert formalizer.formalize("   ") == False

def test_formalize_valid_text(mock_container):
    """Testa formalização de texto válido."""
    formalizer = DescriptionFormalizer(container=mock_container)
    original_text = "Texto para formalizar"
    formalized_text = "Texto formalizado"
    
    formalizer.ai_service.formalize_description.return_value = formalized_text
    
    result = formalizer.formalize(original_text)
    
    assert result == True
    assert formalizer._original_text == original_text
    assert formalizer._formalized_text == formalized_text
    formalizer.ai_service.formalize_description.assert_called_once_with(original_text)

def test_formalize_error(mock_container):
    """Testa erro na formalização."""
    formalizer = DescriptionFormalizer(container=mock_container)
    formalizer.ai_service.formalize_description.side_effect = Exception("AI error")
    
    result = formalizer.formalize("Texto com erro")
    
    assert result == False
    assert formalizer._formalized_text == ""

def test_render_formalizer(mock_streamlit):
    """Testa renderização do formalizador."""
    formalizer = DescriptionFormalizer()
    formalizer.render()
    
    # Verifica se os componentes foram renderizados
    mock_streamlit.write.assert_any_call("### 📝 Formalizador de Descrição")
    mock_streamlit.columns.assert_called_with([3, 1])
    mock_streamlit.text_area.assert_called_once()
    mock_streamlit.toggle.assert_called_once_with("Preview", value=True)
    mock_streamlit.button.assert_called_once()

def test_render_with_formalize_success(mock_streamlit, mock_container):
    """Testa formalização bem-sucedida na interface."""
    formalizer = DescriptionFormalizer(container=mock_container)
    mock_callback = Mock()
    
    # Simula texto e clique no botão
    mock_streamlit.text_area.return_value = "Texto original"
    mock_streamlit.button.side_effect = [True, True, False]  # Formalizar, Aceitar
    formalizer.ai_service.formalize_description.return_value = "Texto formalizado"
    
    formalizer.render(on_save=mock_callback)
    
    # Verifica feedback e callback
    assert mock_streamlit.success.call_count == 2
    mock_streamlit.success.assert_has_calls([
        call("Texto formalizado!"),
        call("Texto salvo!")
    ])
    mock_callback.assert_called_once_with("Texto formalizado")

def test_render_with_reject(mock_streamlit, mock_container):
    """Testa rejeição da formalização."""
    formalizer = DescriptionFormalizer(container=mock_container)
    mock_callback = Mock()
    
    # Simula texto e cliques
    mock_streamlit.text_area.return_value = "Texto original"
    mock_streamlit.button.side_effect = [True, False, True]  # Formalizar, Rejeitar
    formalizer.ai_service.formalize_description.return_value = "Texto formalizado"
    
    formalizer.render(on_save=mock_callback)
    
    # Verifica que o callback não foi chamado e o texto foi limpo
    mock_callback.assert_not_called()
    assert formalizer._formalized_text == ""

def test_formalize_text_too_long(mock_container):
    """Testa rejeição de texto muito longo."""
    formalizer = DescriptionFormalizer(container=mock_container)
    long_text = "a" * (UI_CONFIG['MAX_DESCRIPTION_LENGTH'] + 1)
    
    result = formalizer.formalize(long_text)
    
    assert result == False
    assert formalizer.formalized_text == ""
    formalizer.ai_service.formalize_description.assert_not_called()

def test_clear_texts():
    """Testa limpeza dos textos."""
    formalizer = DescriptionFormalizer()
    formalizer._original_text = "Original"
    formalizer._formalized_text = "Formalizado"
    
    formalizer.clear()
    
    assert formalizer.original_text == ""
    assert formalizer.formalized_text == ""

def test_history_tracking(mock_container):
    """Testa rastreamento do histórico de formalizações."""
    formalizer = DescriptionFormalizer(container=mock_container)
    
    # Primeira formalização
    formalizer.ai_service.formalize_description.return_value = "Texto 1 formalizado"
    formalizer.formalize("Texto 1")
    
    # Segunda formalização
    formalizer.ai_service.formalize_description.return_value = "Texto 2 formalizado"
    formalizer.formalize("Texto 2")
    
    assert len(formalizer._history) == 2
    assert formalizer._history[0] == ("Texto 1", "Texto 1 formalizado")
    assert formalizer._history[1] == ("Texto 2", "Texto 2 formalizado")

def test_render_with_history(mock_streamlit, mock_container):
    """Testa renderização com histórico."""
    formalizer = DescriptionFormalizer(container=mock_container)
    
    # Adiciona algumas formalizações ao histórico
    formalizer._history = [
        ("Original 1", "Formal 1"),
        ("Original 2", "Formal 2")
    ]
    
    formalizer.render()
    
    # Verifica se o histórico foi renderizado
    mock_streamlit.write.assert_any_call("#### Histórico")
    mock_streamlit.expander.assert_called() 