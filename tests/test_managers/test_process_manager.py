import pytest
from src.managers.process_manager import ProcessManager
from src.models.process import Process

@pytest.fixture
def process_manager():
    return ProcessManager()

def test_create_process(process_manager, sample_process_data):
    """Testa a criação de um processo."""
    process = process_manager.create_process(sample_process_data)
    
    assert isinstance(process, Process)
    assert process.name == sample_process_data['process_name']
    assert process_manager.current_process_id == process.name

def test_create_process_invalid_data(process_manager):
    """Testa a criação de processo com dados inválidos."""
    invalid_data = {
        'process_name': '',  # Nome vazio deve falhar
        'process_owner': 'João'
    }
    
    with pytest.raises(ValueError):
        process_manager.create_process(invalid_data)

def test_update_process(process_manager, sample_process_data):
    """Testa a atualização de um processo."""
    process = process_manager.create_process(sample_process_data)
    
    updated_data = {
        'process_name': process.name,
        'steps_as_is': 'Novos passos'
    }
    
    updated_process = process_manager.update_process(process.name, updated_data)
    assert updated_process.steps_as_is == 'Novos passos'

def test_get_process(process_manager, sample_process_data):
    """Testa a recuperação de um processo."""
    process = process_manager.create_process(sample_process_data)
    retrieved = process_manager.get_process(process.name)
    
    assert retrieved is not None
    assert retrieved.name == process.name

def test_list_processes(process_manager, sample_process_data):
    """Testa a listagem de processos."""
    process1 = process_manager.create_process(sample_process_data)
    
    data2 = sample_process_data.copy()
    data2['process_name'] = 'Outro Processo'
    process2 = process_manager.create_process(data2)
    
    processes = process_manager.list_processes()
    assert len(processes) == 2
    assert process1 in processes
    assert process2 in processes 