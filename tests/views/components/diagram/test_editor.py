"""Testes para o editor de diagramas."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.diagram.editor import DiagramEditor
from src.services.ai_service import AIService
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch('src.views.components.diagram.editor.st') as mock_st:
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
    ai_service = Mock(spec=AIService)
    ai_service.generate_diagram.return_value = Mock(code="graph TD\nA-->B")
    container.resolve.return_value = ai_service
    return container

def test_diagram_editor_initialization():
    """Testa inicialização do editor."""
    editor = DiagramEditor()
    assert editor._diagram_code == ""
    assert editor._preview_enabled == True

def test_diagram_editor_with_custom_ai_service(mock_container):
    """Testa inicialização com serviço AI customizado."""
    editor = DiagramEditor(container=mock_container)
    assert editor.container == mock_container
    assert isinstance(editor.ai_service, Mock)

def test_set_invalid_diagram():
    """Testa definição de diagrama inválido."""
    editor = DiagramEditor()
    with pytest.raises(ValueError):
        editor.diagram_code = "invalid"

def test_generate_from_description(mock_container):
    """Testa geração de diagrama a partir de descrição."""
    editor = DiagramEditor(container=mock_container)
    description = "Processo simples"
    steps = ["Início", "Meio", "Fim"]
    
    result = editor.generate_from_description(description, steps)
    
    assert result == True
    assert editor._diagram_code == "graph TD\nA-->B"
    editor.ai_service.generate_diagram.assert_called_once_with(description, steps)

def test_generate_from_description_error(mock_container):
    """Testa erro na geração de diagrama."""
    editor = DiagramEditor(container=mock_container)
    editor.ai_service.generate_diagram.side_effect = Exception("AI error")
    
    result = editor.generate_from_description("desc", ["step"])
    
    assert result == False
    assert editor._diagram_code == ""

def test_render_editor(mock_streamlit):
    """Testa renderização do editor."""
    editor = DiagramEditor()
    editor.render()
    
    mock_streamlit.write.assert_any_call("### 📊 Editor de Diagrama")
    mock_streamlit.columns.assert_called()
    mock_streamlit.text_area.assert_called()

def test_render_with_preview(mock_streamlit):
    """Testa renderização com preview."""
    editor = DiagramEditor()
    editor._diagram_code = "graph TD\nA-->B"
    editor._preview_enabled = True
    
    editor.render()
    
    mock_streamlit.mermaid.assert_called_once_with("graph TD\nA-->B")

def test_render_without_preview(mock_streamlit):
    """Testa renderização sem preview."""
    editor = DiagramEditor()
    editor._diagram_code = "graph TD\nA-->B"
    editor._preview_enabled = False
    
    editor.render()
    
    mock_streamlit.mermaid.assert_not_called() 