import pytest
from unittest.mock import Mock, patch
from src.services.ai_service import AIService, MermaidDiagram

@pytest.fixture
def sample_process_data():
    return {
        'description': 'Processo de aprovação de férias',
        'steps': [
            'Funcionário solicita férias',
            'Gestor analisa pedido',
            'RH valida período',
            'Sistema atualiza banco de horas'
        ]
    }

@pytest.fixture
def mock_successful_response():
    return """```mermaid
    flowchart TD
        p1[Funcionário solicita férias] --> p2[Gestor analisa pedido]
        p2 --> p3[RH valida período]
        p3 --> p4[Sistema atualiza banco de horas]
    ```
    
    Explicação:
    O fluxo representa o processo de aprovação de férias."""

def test_generate_diagram_empty_input():
    """Testa a geração de diagrama com inputs vazios."""
    service = AIService()
    
    with pytest.raises(ValueError, match="Descrição do processo e passos são obrigatórios"):
        service.generate_diagram("", [])

@patch('langchain.chains.LLMChain')
@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_success(mock_chat, mock_chain, sample_process_data, mock_successful_response):
    """Testa a geração bem-sucedida de diagrama."""
    # Configura o mock da chain
    chain_instance = Mock()
    chain_instance.invoke.return_value = {'text': mock_successful_response}
    mock_chain.return_value = chain_instance
    
    service = AIService()
    result = service.generate_diagram(
        sample_process_data['description'],
        sample_process_data['steps']
    )
    
    assert isinstance(result, MermaidDiagram)
    assert "flowchart TD" in result.diagram_code
    assert len(result.explanation) > 0

@patch('langchain.chains.LLMChain')
@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_invalid_response(mock_chat, mock_chain, sample_process_data):
    """Testa a geração de diagrama com resposta inválida da IA."""
    # Configura o mock da chain
    chain_instance = Mock()
    chain_instance.invoke.return_value = {'text': 'Resposta inválida sem diagrama'}
    mock_chain.return_value = chain_instance
    
    service = AIService()
    with pytest.raises(ValueError, match="Não foi possível extrair o diagrama da resposta"):
        service.generate_diagram(
            sample_process_data['description'],
            sample_process_data['steps']
        )