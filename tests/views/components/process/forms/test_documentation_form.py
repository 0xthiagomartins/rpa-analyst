"""Testes para o formulário de documentação."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.process.forms.documentation_form import DocumentationForm
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.process.forms.documentation_form.st") as mock_st:
        # Simula colunas
        col1, col2, col3 = Mock(), Mock(), Mock()
        
        # Corrige o side_effect para aceitar tanto int quanto list
        def columns_side_effect(spec):
            if isinstance(spec, (int, list)):
                # Retorna sempre 2 colunas quando recebe uma lista [4, 1]
                if isinstance(spec, list) and len(spec) == 2:
                    return [col1, col2]
                # Retorna 3 colunas apenas quando explicitamente pedido
                return [col1, col2, col3] if spec == 3 else [col1, col2]
            return [col1, col2]
            
        mock_st.columns.side_effect = columns_side_effect
        
        # Simula contexto das colunas
        for col in [col1, col2, col3]:
            col.__enter__ = lambda x: col
            col.__exit__ = lambda x, y, z, w: None
        
        # Configura retornos padrão
        mock_st.text_input.return_value = ""
        mock_st.text_area.return_value = ""
        mock_st.selectbox.return_value = "Manual"
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

def test_documentation_form_initialization(mock_container):
    """Testa inicialização do formulário."""
    form = DocumentationForm(mock_container)
    assert form._data == {}
    assert form.container == mock_container

def test_documentation_form_validation_success(mock_container):
    """Testa validação com sucesso."""
    form = DocumentationForm(mock_container)
    form._data = {
        "documents": [{
            "title": "Manual do Processo",
            "type": "Manual",
            "version": "1.0",
            "status": "Aprovado",
            "description": "Manual completo"
        }],
        "references": [{
            "title": "Documentação API",
            "type": "Link",
            "url": "https://api.docs"
        }]
    }
    
    assert form.validate() == True
    form.validator.validate_form.assert_called_once()

def test_documentation_form_validation_failure(mock_container, mock_streamlit):
    """Testa falha na validação."""
    form = DocumentationForm(mock_container)
    form.validator.validate_form.return_value = [Mock(message="Erro")]
    
    assert form.validate() == False
    mock_streamlit.error.assert_called_once()

def test_add_document(mock_container, mock_streamlit):
    """Testa adição de documento."""
    form = DocumentationForm(mock_container)
    mock_streamlit.text_input.side_effect = ["Manual do Processo", "1.0"]
    mock_streamlit.selectbox.side_effect = ["Manual", "Aprovado"]
    mock_streamlit.text_area.return_value = "Manual completo"
    mock_streamlit.button.return_value = True
    
    form._add_document(form._data.setdefault("documents", []))
    
    assert {
        "title": "Manual do Processo",
        "type": "Manual",
        "version": "1.0",
        "status": "Aprovado",
        "description": "Manual completo"
    } in form._data["documents"]

def test_add_reference(mock_container, mock_streamlit):
    """Testa adição de referência."""
    form = DocumentationForm(mock_container)
    mock_streamlit.text_input.side_effect = ["Documentação API", "https://api.docs"]
    mock_streamlit.selectbox.return_value = "Link"
    mock_streamlit.button.return_value = True
    
    form._add_reference(form._data.setdefault("references", []))
    
    assert {
        "title": "Documentação API",
        "type": "Link",
        "url": "https://api.docs"
    } in form._data["references"]

def test_render_form(mock_container, mock_streamlit):
    """Testa renderização do formulário."""
    form = DocumentationForm(mock_container)
    form._data = {
        "documents": [{
            "title": "Manual do Processo",
            "type": "Manual",
            "version": "1.0",
            "status": "Aprovado",
            "description": "Manual completo"
        }],
        "references": [{
            "title": "Documentação API",
            "type": "Link",
            "url": "https://api.docs"
        }]
    }
    
    form.render()
    
    # Verifica se os títulos foram renderizados
    mock_streamlit.write.assert_any_call("### 📚 Documentação e Referências")
    mock_streamlit.write.assert_any_call("#### Documentos")
    mock_streamlit.write.assert_any_call("#### Referências") 