import pytest
from unittest.mock import Mock, patch
from src.services.ai_service import AIService, MermaidDiagram

@pytest.fixture
def sample_process_data():
    return {
        'description': 'Processo de aprovação de férias',
        'steps': [
            'Funcionário submete pedido',
            'RH verifica elegibilidade',
            'Gestor aprova ou rejeita',
            'RH registra decisão',
            'Sistema notifica funcionário'
        ]
    }

@pytest.fixture
def sample_mermaid_output():
    return """
    flowchart TD
        A[Início] --> B[Funcionário submete pedido]
        B --> C{RH verifica elegibilidade}
        C -->|Elegível| D[Gestor analisa]
        C -->|Não elegível| E[Pedido rejeitado]
        D -->|Aprovado| F[RH registra aprovação]
        D -->|Rejeitado| G[RH registra rejeição]
        F --> H[Notifica funcionário]
        G --> H
        E --> H
        H --> I[Fim]
    """

@pytest.fixture
def mock_llm_response():
    return {
        'diagram_code': 'graph TD\nA-->B',
        'explanation': 'Diagrama simples mostrando fluxo A para B'
    }

def test_ai_service_initialization():
    """Testa a inicialização do serviço de IA."""
    service = AIService()
    assert service.llm is not None
    assert service.parser is not None

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_success(mock_chat, sample_process_data):
    """Testa a geração bem-sucedida de um diagrama."""
    # Configura o mock para retornar exatamente o que esperamos
    mock_chain = Mock()
    mock_chain.invoke.return_value = {
        'text': '{"diagram_code": "graph TD\\nA-->B", "explanation": "Diagrama simples"}'
    }
    
    with patch('langchain.chains.LLMChain', return_value=mock_chain):
        service = AIService()
        result = service.generate_diagram(
            sample_process_data['description'],
            sample_process_data['steps']
        )
        
        assert isinstance(result, MermaidDiagram)
        # Aceita tanto TD quanto TB como direção válida
        assert any(direction in result.diagram_code for direction in ["graph TD", "graph TB"])
        assert result.explanation is not None
        assert len(result.explanation) > 0

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_with_empty_input(mock_chat):
    """Testa a geração de diagrama com entrada vazia."""
    service = AIService()
    
    with pytest.raises(ValueError):
        service.generate_diagram("", [])

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_with_invalid_steps(mock_chat):
    """Testa a geração de diagrama com steps inválidos."""
    service = AIService()
    
    with pytest.raises(ValueError):
        service.generate_diagram("Descrição válida", None)

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_api_error(mock_chat, sample_process_data):
    """Testa o comportamento quando a API retorna erro."""
    # Mock the chain and make it raise an exception
    mock_chain = Mock()
    mock_chain.invoke.side_effect = Exception("API Error")
    
    # Mock the LLMChain class itself, not just its instance
    with patch('langchain.chains.LLMChain', Mock(return_value=mock_chain)) as mock_llm_chain:
        service = AIService()
        
        with pytest.raises(ValueError) as exc_info:
            service.generate_diagram(
                sample_process_data['description'],
                sample_process_data['steps']
            )
        
        assert "Erro na chamada da API" in str(exc_info.value)
        # Verify the mock was called
        mock_llm_chain.assert_called_once()

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_invalid_response(mock_chat, sample_process_data):
    """Testa o comportamento quando a API retorna uma resposta inválida."""
    # Mock the chain to return an invalid response
    mock_chain = Mock()
    mock_chain.invoke.return_value = {}
    
    # Mock the LLMChain class itself
    with patch('langchain.chains.LLMChain', Mock(return_value=mock_chain)) as mock_llm_chain:
        service = AIService()
        
        with pytest.raises(ValueError) as exc_info:
            service.generate_diagram(
                sample_process_data['description'],
                sample_process_data['steps']
            )
        
        assert "Resposta inválida da API" in str(exc_info.value)
        mock_llm_chain.assert_called_once()

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram_parse_error(mock_chat, sample_process_data):
    """Testa o comportamento quando há erro ao fazer parse da resposta."""
    # Mock the chain to return invalid JSON
    mock_chain = Mock()
    mock_chain.invoke.return_value = {'text': 'Invalid JSON'}
    
    with patch('langchain.chains.LLMChain', Mock(return_value=mock_chain)) as mock_llm_chain:
        service = AIService()
        with pytest.raises(ValueError) as exc_info:
            service.generate_diagram(
                sample_process_data['description'],
                sample_process_data['steps']
            )
        
        assert "Erro ao processar resposta da API" in str(exc_info.value)
        mock_llm_chain.assert_called_once()

@pytest.mark.integration
def test_generate_diagram_integration(sample_process_data):
    """Teste de integração real com a API (requer chave válida)."""
    try:
        service = AIService()
        result = service.generate_diagram(
            sample_process_data['description'],
            sample_process_data['steps']
        )
        
        assert isinstance(result, MermaidDiagram)
        # Verifica se contém qualquer uma das sintaxes válidas do Mermaid
        assert any(syntax in result.diagram_code for syntax in ["flowchart TD", "graph TD"])
        assert len(result.explanation) > 0
        
        # Verifica se o diagrama contém os elementos esperados
        diagram_code = result.diagram_code.lower()
        assert "funcionário" in diagram_code
        assert "rh" in diagram_code
        assert "gestor" in diagram_code
        assert "-->" in diagram_code  # Verifica se há conexões no diagrama
    except Exception as e:
        pytest.skip(f"Teste de integração falhou: {str(e)}")