import pytest
from unittest.mock import Mock, patch
from src.services.document_service import DocumentService

@pytest.fixture
def mock_ai_service():
    """Mock do AIService."""
    mock = Mock()
    mock.analyze_process_description.return_value = {
        "steps": [
            {
                "id": "node_0",
                "name": "Início",
                "type": "start",
                "description": "Início do processo"
            }
        ],
        "connections": [],
        "process_analysis": {
            "start_node": "node_0",
            "end_nodes": [],
            "conditional_paths": []
        },
        "details": {
            "steps": ["Passo 1"],
            "tools": ["Ferramenta 1"],
            "data_types": ["Tipo 1"],
            "data_formats": ["Formato 1"],
            "data_sources": ["Fonte 1"],
            "data_volume": "Baixo"
        },
        "business_rules": {
            "business_rules": ["Regra 1"],
            "exceptions": ["Exceção 1"]
        },
        "automation_goals": {
            "automation_goals": ["Objetivo 1"],
            "kpis": ["KPI 1"]
        }
    }
    return mock

@pytest.fixture
def document_service(mock_ai_service):
    """Fixture para o DocumentService com AIService mockado."""
    with patch('src.services.document_service.AIService', return_value=mock_ai_service):
        return DocumentService()

def test_generate_pdd(document_service):
    """Testa geração de PDD."""
    process_data = {
        "process_name": "Processo Teste",
        "process_owner": "Dono Teste",
        "process_description": "Descrição teste",
        "steps_as_is": ["Passo 1"],
        "systems": ["Sistema 1"],
        "data_used": {
            "types": ["Tipo 1"],
            "formats": ["Formato 1"],
            "sources": ["Fonte 1"]
        },
        "business_rules": ["Regra 1"],
        "exceptions": ["Exceção 1"],
        "automation_goals": ["Objetivo 1"],
        "kpis": ["KPI 1"]
    }
    
    # Mock das dependências do DocumentService
    with patch('src.services.document_service.SimpleDocTemplate') as mock_doc, \
         patch('src.services.document_service.os.path.join', return_value='test.pdf'), \
         patch('src.services.document_service.os.makedirs'):
        
        # Configura o mock do SimpleDocTemplate
        mock_doc.return_value.build.return_value = None
        
        result = document_service.generate_pdd(process_data)
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith('.pdf')
        assert "Processo_Teste" in result 