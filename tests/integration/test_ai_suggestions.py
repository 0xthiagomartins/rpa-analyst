"""Testes de integração para o sistema de sugestões."""
import pytest
from unittest.mock import AsyncMock, patch
from src.services.ai_service import AIService
from src.services.validator_service import ValidatorService
from src.utils.cache import InMemoryCache

@pytest.fixture
def services():
    """Fixture com todos os serviços necessários."""
    validator = ValidatorService()
    ai_service = AIService(validator=validator)
    cache = InMemoryCache()
    return {
        "validator": validator,
        "ai_service": ai_service,
        "cache": cache
    }

@pytest.mark.asyncio
async def test_full_suggestion_flow(services):
    """Testa fluxo completo de sugestões."""
    mock_response = {
        "choices": [{
            "message": {
                "content": """{
                    "description": "Processo otimizado de análise de crédito",
                    "forms_data": {
                        "identification": {
                            "form_id": "identification",
                            "is_valid": true,
                            "has_changes": true,
                            "data": {
                                "name": "Análise de Crédito v2",
                                "responsible": "Equipe Financeiro",
                                "area": "Financeiro"
                            }
                        },
                        "steps": {
                            "form_id": "steps",
                            "is_valid": true,
                            "has_changes": true,
                            "data": {
                                "steps": [
                                    {
                                        "name": "Validação Inicial",
                                        "system": "Oracle"
                                    }
                                ]
                            }
                        },
                        "systems": {
                            "form_id": "systems",
                            "is_valid": true,
                            "has_changes": true,
                            "data": {
                                "systems": [
                                    {
                                        "name": "Oracle",
                                        "type": "ERP"
                                    }
                                ]
                            }
                        }
                    },
                    "suggestions": [
                        "Adicionar validação automatizada",
                        "Integrar com sistema antifraude"
                    ],
                    "validation": []
                }"""
            }
        }]
    }

    mock_acreate = AsyncMock(return_value=mock_response)

    with patch('openai.ChatCompletion.acreate', new=mock_acreate):
        # Dados atuais do processo
        current_data = {
            "name": "Análise de Crédito",
            "responsible": "João Silva",
            "steps": []
        }

        # Solicita sugestões
        result = await services["ai_service"].suggest_improvements(
            "Processo manual de análise de crédito",
            current_data
        )

        # Verifica estrutura da resposta
        assert "description" in result
        assert "forms_data" in result
        assert "suggestions" in result
        assert "validation" in result

        # Verifica dados específicos
        forms_data = result["forms_data"]
        assert "identification" in forms_data
        assert "steps" in forms_data
        assert "systems" in forms_data

        # Verifica relacionamentos
        steps = forms_data["steps"]["data"]["steps"]
        systems = forms_data["systems"]["data"]["systems"]
        for step in steps:
            if "system" in step:
                system_names = [s["name"] for s in systems]
                assert step["system"] in system_names

@pytest.mark.asyncio
async def test_invalid_suggestion_handling(services):
    """Testa tratamento de sugestões inválidas."""
    mock_response = {
        "choices": [{
            "message": {
                "content": """{
                    "description": "Processo inválido",
                    "forms_data": {
                        "steps": {
                            "data": {
                                "steps": [
                                    {
                                        "name": "Passo 1",
                                        "system": "Sistema Inexistente"
                                    }
                                ]
                            }
                        },
                        "systems": {
                            "data": {
                                "systems": []
                            }
                        }
                    },
                    "suggestions": [],
                    "validation": []
                }"""
            }
        }]
    }

    mock_acreate = AsyncMock(return_value=mock_response)

    with patch('openai.ChatCompletion.acreate', new=mock_acreate):
        with pytest.raises(ValueError) as exc_info:
            await services["ai_service"].suggest_improvements(
                "Processo com erro",
                {}
            )
        
        assert "Sistema Inexistente" in str(exc_info.value) 