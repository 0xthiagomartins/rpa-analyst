import pytest
from src.templates.pdd_template import PDDTemplate

@pytest.fixture
def pdd_template():
    return PDDTemplate()

def test_validate_data(pdd_template, sample_process_data):
    """Testa a validação dos dados do template."""
    assert pdd_template.validate_data(sample_process_data)
    
    # Teste com dados incompletos
    invalid_data = {'process_name': 'Teste'}
    assert not pdd_template.validate_data(invalid_data)

def test_render_template(pdd_template, sample_process_data):
    """Testa a renderização do template."""
    rendered = pdd_template.render(sample_process_data)
    
    assert sample_process_data['process_name'] in rendered
    assert sample_process_data['process_owner'] in rendered
    assert sample_process_data['process_description'] in rendered

def test_render_invalid_data(pdd_template):
    """Testa a renderização com dados inválidos."""
    invalid_data = {'process_name': 'Teste'}
    
    with pytest.raises(ValueError):
        pdd_template.render(invalid_data) 