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

@patch('langchain_openai.ChatOpenAI')
def test_generate_diagram(mock_chat, sample_process_data):
    """Testa a geração de diagrama - caminho feliz e casos de erro."""
    
    # Caso 1: Geração bem-sucedida
    mock_response = """```mermaid
    flowchart TD
        p1[Funcionário solicita férias] --> p2[Gestor analisa pedido]
        p2 --> p3[RH valida período]
        p3 --> p4[Sistema atualiza banco de horas]
    ```
    
    Explicação:
    O fluxo representa o processo de aprovação de férias.
    """
    
    mock_chain = Mock()
    mock_chain.invoke.return_value = {'text': mock_response}
    
    with patch('langchain.chains.LLMChain', Mock(return_value=mock_chain)):
        service = AIService()
        
        # Testa inputs inválidos
        with pytest.raises(ValueError):
            service.generate_diagram("", [])
        
        with pytest.raises(ValueError):
            service.generate_diagram("descrição", [])
        
        # Testa geração bem-sucedida
        result = service.generate_diagram(
            sample_process_data['description'],
            sample_process_data['steps']
        )
        
        assert isinstance(result, MermaidDiagram)
        assert "flowchart TD" in result.diagram_code
        assert len(result.explanation) > 0
        
        # Testa resposta inválida da IA
        mock_chain.invoke.return_value = {'text': 'Resposta inválida'}
        with pytest.raises(ValueError):
            service.generate_diagram(
                sample_process_data['description'],
                sample_process_data['steps']
            )