import pytest
from unittest.mock import Mock, patch
from src.services.ai_service import AIService, MermaidDiagram

@pytest.fixture
def mock_llm():
    """Mock do LLM."""
    mock = Mock()
    mock.invoke = Mock(return_value={"content": """```mermaid
    flowchart TD
        A[Início] --> B[Fim]
    ```
    
    Explicação:
    Fluxo básico de teste."""})
    return mock

@pytest.fixture
def ai_service(mock_llm):
    """Fixture para o AIService com LLM mockado."""
    return AIService(llm=mock_llm)

def test_generate_diagram_success(ai_service):
    """Testa geração bem-sucedida de diagrama."""
    description = "Processo de teste"
    steps = ["Passo 1", "Passo 2"]
    
    # Mock do ChatPromptTemplate
    mock_prompt = Mock()
    mock_prompt.format_messages.return_value = [{"content": description}]
    
    with patch('langchain.prompts.ChatPromptTemplate.from_template', return_value=mock_prompt):
        result = ai_service.generate_diagram(description, steps)
        
        assert isinstance(result, MermaidDiagram)
        assert "flowchart TD" in result.diagram_code
        assert result.explanation != ""

def test_generate_diagram_invalid_response(ai_service):
    """Testa geração de diagrama com resposta inválida."""
    description = "Processo de teste"
    steps = ["Passo 1", "Passo 2"]
    
    # Mock do ChatPromptTemplate
    mock_prompt = Mock()
    mock_prompt.format_messages.return_value = [{"content": description}]
    
    # Força uma resposta inválida
    ai_service.llm.invoke.return_value = {"content": "resposta inválida sem diagrama"}
    
    with patch('langchain.prompts.ChatPromptTemplate.from_template', return_value=mock_prompt):
        with pytest.raises(ValueError, match="Não foi possível extrair o diagrama da resposta"):
            ai_service.generate_diagram(description, steps)