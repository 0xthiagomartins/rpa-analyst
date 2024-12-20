import pytest
from src.controllers.process_controller import ProcessController

@pytest.fixture
def process_controller():
    return ProcessController()

def test_create_process(process_controller, sample_process_data):
    """Testa a criação de um processo através do controller."""
    process = process_controller.create_process(sample_process_data)
    
    assert process.name == sample_process_data['process_name']
    assert process.owner == sample_process_data['process_owner']
    assert process_controller.get_current_process() is not None

def test_update_process(process_controller, sample_process_data):
    """Testa a atualização de um processo existente."""
    process = process_controller.create_process(sample_process_data)
    
    updated_data = sample_process_data.copy()
    updated_data['steps_as_is'] = 'Novos passos'
    
    updated_process = process_controller.update_process(updated_data)
    assert updated_process.steps_as_is == 'Novos passos'

def test_get_current_process(process_controller, sample_process_data):
    """Testa a recuperação do processo atual."""
    assert process_controller.get_current_process() is None
    
    process = process_controller.create_process(sample_process_data)
    current_process = process_controller.get_current_process()
    
    assert current_process is not None
    assert current_process.name == process.name