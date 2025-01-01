"""Testes para o componente DataPreview."""
import pytest
from unittest.mock import Mock, patch
from src.views.components.preview.data_preview import DataPreview

@pytest.fixture
def mock_streamlit():
    """Mock para o Streamlit."""
    with patch("src.views.components.preview.data_preview.st") as mock_st:
        # Simula expander
        expander = Mock()
        expander.__enter__ = Mock(return_value=expander)
        expander.__exit__ = Mock(return_value=None)
        mock_st.expander.return_value = expander
        
        # Simula colunas com suporte a context manager
        col1, col2 = Mock(), Mock()
        col1.__enter__ = Mock(return_value=col1)
        col1.__exit__ = Mock(return_value=None)
        col2.__enter__ = Mock(return_value=col2)
        col2.__exit__ = Mock(return_value=None)
        
        mock_st.columns.return_value = [col1, col2]
        
        yield mock_st

def test_render_with_data(mock_streamlit):
    """Testa renderização com dados."""
    preview = DataPreview("test_form")
    data = {
        "process_name": "Teste",
        "owner": "João",
        "description": "Descrição teste"
    }
    
    preview.render(data)
    
    # Verifica se expander foi criado
    mock_streamlit.expander.assert_called_once()
    
    # Verifica se colunas foram criadas para cada campo
    assert mock_streamlit.columns.call_count == len(data)
    
    # Verifica se os dados foram escritos
    cols = mock_streamlit.columns.return_value
    assert cols[0].write.call_count == len(data)  # Títulos dos campos
    assert cols[1].write.call_count == len(data)  # Valores dos campos

def test_render_empty_data(mock_streamlit):
    """Testa renderização sem dados."""
    preview = DataPreview("test_form")
    
    preview.render({})
    
    mock_streamlit.info.assert_called_once_with("Nenhum dado preenchido ainda") 