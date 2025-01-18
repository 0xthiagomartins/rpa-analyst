"""Testes para o ValidatorService."""
import pytest
from src.services.validator_service import ValidatorService, ValidationResult

@pytest.fixture
def validator():
    """Fixture que fornece uma instância do ValidatorService."""
    return ValidatorService()

@pytest.fixture
def valid_suggestions():
    """Fixture que fornece sugestões válidas."""
    return {
        "description": "Processo de aprovação de despesas",
        "forms_data": {
            "identification": {
                "data": {
                    "name": "Aprovação de Despesas",
                    "owner": "Financeiro"
                }
            }
        },
        "suggestions": ["Sugestão 1", "Sugestão 2"],
        "validation": []
    }

def test_validate_valid_suggestions(validator, valid_suggestions):
    """Testa validação de sugestões válidas."""
    result = validator.validate_suggestions(valid_suggestions)
    assert result.is_valid
    assert not result.errors
    
def test_validate_missing_required_fields(validator):
    """Testa validação com campos obrigatórios ausentes."""
    invalid_suggestions = {
        "description": "Teste",
        # forms_data ausente
        "suggestions": []
    }
    
    result = validator.validate_suggestions(invalid_suggestions)
    assert not result.is_valid
    assert any("forms_data" in error for error in result.errors)

def test_validate_invalid_form_data(validator):
    """Testa validação com dados de formulário inválidos."""
    invalid_suggestions = {
        "description": "Teste",
        "forms_data": {
            "identification": "não é um dict"  # Deveria ser um dict
        },
        "suggestions": [],
        "validation": []
    }
    
    result = validator.validate_suggestions(invalid_suggestions)
    assert not result.is_valid
    assert any("identification" in error for error in result.errors)

def test_validate_steps_systems_relationship(validator):
    """Testa validação de relacionamento entre passos e sistemas."""
    suggestions = {
        "description": "Teste",
        "forms_data": {
            "steps": {
                "data": {
                    "steps": [
                        {"name": "Passo 1", "system": "SAP"}
                    ]
                }
            },
            "systems": {
                "data": {
                    "systems": [
                        {"name": "Oracle"}  # SAP não está definido
                    ]
                }
            }
        },
        "suggestions": [],
        "validation": []
    }
    
    result = validator.validate_suggestions(suggestions)
    assert not result.is_valid
    assert any("SAP" in error for error in result.errors) 