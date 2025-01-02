"""Testes para o validador de sugestões."""
import pytest
from datetime import datetime
from src.views.components.suggestions.suggestion_validator import (
    SuggestionValidator,
    ValidationResult
)
from src.views.components.suggestions.suggestions_buffer import SuggestionData

@pytest.fixture
def validator():
    """Fixture que fornece uma instância do validador."""
    return SuggestionValidator()

@pytest.fixture
def valid_suggestion():
    """Fixture que fornece uma sugestão válida."""
    return SuggestionData(
        form_id="identification",
        data={
            "form_id": "identification",
            "data": {
                "process_name": "Processo Teste",
                "responsible": "João Silva",
                "department": "TI"
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )

def test_validate_valid_suggestion(validator, valid_suggestion):
    """Testa validação de sugestão válida."""
    result = validator.validate_suggestion(valid_suggestion)
    
    assert result.is_valid
    assert not result.errors
    assert isinstance(result, ValidationResult)

def test_validate_invalid_structure(validator):
    """Testa validação com estrutura inválida."""
    invalid_suggestion = SuggestionData(
        form_id="identification",
        data="dados inválidos",  # Deveria ser um dict
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(invalid_suggestion)
    
    assert not result.is_valid
    assert "Estrutura de dados inválida" in result.errors

def test_validate_missing_required_fields(validator):
    """Testa validação com campos obrigatórios faltando."""
    suggestion = SuggestionData(
        form_id="identification",
        data={
            "form_id": "identification",
            "data": {
                "process_name": "Processo Teste"
                # Faltam campos obrigatórios
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(suggestion)
    
    assert not result.is_valid
    assert any("obrigatório" in error for error in result.errors)

def test_validate_process_details(validator):
    """Testa validação do formulário de detalhes."""
    suggestion = SuggestionData(
        form_id="process_details",
        data={
            "form_id": "process_details",
            "data": {
                "objective": "Objetivo teste",
                "scope": "Escopo teste",
                "systems": ["Sistema 1", "Sistema 2"]
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(suggestion)
    assert result.is_valid

def test_validate_business_rules(validator):
    """Testa validação do formulário de regras."""
    suggestion = SuggestionData(
        form_id="business_rules",
        data={
            "form_id": "business_rules",
            "data": {
                "rules": ["Regra 1", "Regra 2"]
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(suggestion)
    assert result.is_valid

def test_validate_systems(validator):
    """Testa validação do formulário de sistemas."""
    suggestion = SuggestionData(
        form_id="systems",
        data={
            "form_id": "systems",
            "data": {
                "systems": [
                    {
                        "name": "SAP",
                        "type": "ERP",
                        "access_type": "Direct",
                        "description": "Sistema principal"
                    }
                ],
                "integrations": [
                    {
                        "source": "SAP",
                        "target": "Excel",
                        "type": "Export",
                        "description": "Exportação de relatórios"
                    }
                ]
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(suggestion)
    assert result.is_valid

def test_validate_invalid_systems(validator):
    """Testa validação com sistemas inválidos."""
    suggestion = SuggestionData(
        form_id="systems",
        data={
            "form_id": "systems",
            "data": {
                "systems": [
                    {
                        "name": "SAP"
                        # Faltam campos obrigatórios
                    }
                ]
            },
            "timestamp": datetime.now()
        },
        confidence=0.9,
        timestamp=datetime.now()
    )
    
    result = validator.validate_suggestion(suggestion)
    assert not result.is_valid
    assert any("obrigatório" in error for error in result.errors) 