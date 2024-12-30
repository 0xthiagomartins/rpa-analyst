"""Testes para os validadores do sistema."""
import pytest
from src.utils.validators import (
    validate_process_name,
    validate_process_description,
    validate_diagram,
    validate_required_fields
)

def test_validate_process_name():
    """Testa a validação do nome do processo."""
    # Caso válido
    assert validate_process_name("Processo de Vendas") == True
    
    # Casos inválidos
    assert validate_process_name("") == False  # Vazio
    assert validate_process_name(" ") == False  # Apenas espaços
    assert validate_process_name("a" * 101) == False  # Muito longo

def test_validate_process_description():
    """Testa a validação da descrição do processo."""
    # Caso válido
    assert validate_process_description("Descrição válida do processo") == True
    
    # Casos inválidos
    assert validate_process_description("") == False  # Vazio
    assert validate_process_description(" ") == False  # Apenas espaços
    assert validate_process_description("a" * 5001) == False  # Muito longo

def test_validate_diagram():
    """Testa a validação do diagrama."""
    valid_diagram = """
    graph TD
    A[Início] --> B[Processo]
    B --> C[Fim]
    """
    
    invalid_diagram = """
    graph TD
    A[Início] --> 
    """
    
    # Caso válido
    assert validate_diagram(valid_diagram) == True
    
    # Casos inválidos
    assert validate_diagram("") == False  # Vazio
    assert validate_diagram(invalid_diagram) == False  # Sintaxe inválida

def test_validate_required_fields():
    """Testa a validação de campos obrigatórios."""
    # Caso válido
    data = {
        "name": "Processo",
        "description": "Descrição",
        "owner": "João"
    }
    required = ["name", "description", "owner"]
    assert validate_required_fields(data, required) == True
    
    # Casos inválidos
    invalid_data = {
        "name": "Processo",
        "description": ""  # Campo vazio
    }
    assert validate_required_fields(invalid_data, required) == False
    
    missing_data = {
        "name": "Processo"  # Faltam campos
    }
    assert validate_required_fields(missing_data, required) == False 