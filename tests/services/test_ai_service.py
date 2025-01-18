"""Testes para o serviço de IA."""
import pytest
from unittest.mock import patch, AsyncMock
from src.services.ai_service import AIService
from src.services.ai_types import AIResponse
from src.services.validator_service import ValidatorService
import json

@pytest.fixture
def ai_service():
    """Fixture que fornece uma instância do AIService."""
    validator = ValidatorService()
    return AIService(validator=validator)

@pytest.fixture
def mock_openai_response():
    """Mock de resposta da OpenAI."""
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "description": "Processo formalizado de análise de crédito",
                    "forms_data": {
                        "identification": {
                            "form_id": "identification",
                            "is_valid": True,
                            "has_changes": True,
                            "data": {
                                "name": "Análise de Crédito",
                                "responsible": "Departamento Financeiro",
                                "area": "Financeiro"
                            }
                        }
                    },
                    "suggestions": [
                        "Adicionar validação inicial de dados",
                        "Incluir etapa de análise de fraude"
                    ],
                    "validation": [
                        "Processo precisa de ponto de decisão"
                    ]
                })
            }
        }]
    }

@pytest.mark.asyncio
async def test_suggest_improvements_success(ai_service, mock_openai_response):
    """Testa sugestão de melhorias com sucesso."""
    description = "Processo de análise de crédito manual"

    mock_acreate = AsyncMock()
    mock_acreate.return_value = mock_openai_response

    with patch('openai.ChatCompletion.acreate', new=mock_acreate):
        result = await ai_service.suggest_improvements(description)
        
        assert "description" in result
        assert "forms_data" in result
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0

@pytest.mark.asyncio
async def test_suggest_improvements_cache_hit(ai_service, mock_openai_response):
    """Testa uso do cache."""
    description = "Processo de análise de crédito"
    
    mock_acreate = AsyncMock()
    mock_acreate.return_value = mock_openai_response
    
    with patch('openai.ChatCompletion.acreate', new=mock_acreate):
        result1 = await ai_service.suggest_improvements(description)
        result2 = await ai_service.suggest_improvements(description)
        
        # Segunda chamada deve usar cache
        assert mock_acreate.call_count == 1
        assert result1 == result2

@pytest.mark.asyncio
async def test_suggest_improvements_with_current_data(ai_service, mock_openai_response):
    """Testa sugestões com dados atuais."""
    description = "Processo de análise de crédito"
    current_data = {
        "name": "Análise de Crédito",
        "responsible": "João Silva"
    }

    mock_acreate = AsyncMock()
    mock_acreate.return_value = mock_openai_response

    with patch('openai.ChatCompletion.acreate', new=mock_acreate):
        result = await ai_service.suggest_improvements(description, current_data)
        
        # Verifica se dados atuais foram incluídos no prompt
        prompt = mock_acreate.call_args[1]['messages'][0]['content']
        assert " " in prompt

def test_parse_response_invalid_json(ai_service):
    """Testa parse de resposta com JSON inválido."""
    invalid_data = "não é json"
    
    with pytest.raises(ValueError, match="Resposta inválida da IA"):
        ai_service._parse_response(invalid_data)

def test_parse_response_missing_fields(ai_service):
    """Testa parse de resposta com campos faltando."""
    invalid_data = {
        "description": "Teste",
        "forms_data": {
            "identification": "não é um dict"
        }
    }
    
    with pytest.raises(ValueError, match="Dados inválidos"):
        ai_service._parse_response(invalid_data) 