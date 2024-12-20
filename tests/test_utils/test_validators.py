import pytest
from src.utils.validators import FormValidator, ValidationError

def test_validate_required_fields(form_validator):
    """Testa a validação de campos obrigatórios."""
    data = {'field1': 'value1', 'field2': ''}
    required_fields = ['field1', 'field2', 'field3']
    
    is_valid, missing_fields = form_validator.validate_required_fields(data, required_fields)
    
    assert not is_valid
    assert 'field2' in missing_fields
    assert 'field3' in missing_fields

def test_validate_email(form_validator):
    """Testa a validação de email."""
    assert form_validator.validate_email('user@example.com')
    assert not form_validator.validate_email('invalid-email')
    assert not form_validator.validate_email('')

def test_validate_length(form_validator):
    """Testa a validação de comprimento de texto."""
    assert form_validator.validate_length('text', min_length=2)
    assert not form_validator.validate_length('a', min_length=2)
    assert form_validator.validate_length('text', min_length=1, max_length=5)
    assert not form_validator.validate_length('text', min_length=1, max_length=3)

def test_validate_form(form_validator):
    """Testa a validação completa de um formulário."""
    # Teste com campo obrigatório vazio
    data = {
        'process_name': 'Teste',
        'process_owner': '',  # Campo obrigatório vazio
        'process_description': 'Descrição'
    }
    
    errors = form_validator.validate_form(data, 'identification')
    assert len(errors) > 0
    assert any(error.field == 'process_owner' for error in errors)
    
    # Teste com todos os campos preenchidos
    data_valid = {
        'process_name': 'Teste',
        'process_owner': 'João',
        'process_description': 'Descrição'
    }
    errors_valid = form_validator.validate_form(data_valid, 'identification')
    assert len(errors_valid) == 0
    
    # Teste com campo faltando
    data_missing = {
        'process_name': 'Teste'
        # process_owner e process_description faltando
    }
    errors_missing = form_validator.validate_form(data_missing, 'identification')
    assert len(errors_missing) == 2