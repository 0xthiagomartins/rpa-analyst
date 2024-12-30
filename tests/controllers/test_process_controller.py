"""Testes para o controller de processos."""
import pytest
from unittest.mock import Mock, patch
from src.controllers.process_controller import ProcessController
from src.managers.process_manager import ProcessManager
from src.services.ai_service import AIService
from src.utils.dependency_container import DependencyContainer

@pytest.fixture
def mock_container():
    """Fixture para simular o container."""
    container = Mock(spec=DependencyContainer)
    
    # Cria mock do ProcessManager com todos os métodos necessários
    process_manager = Mock(spec=ProcessManager)
    process_manager.create_process = Mock(return_value=True)
    process_manager.update_process = Mock(return_value=True)
    process_manager.get_process = Mock(return_value={})
    process_manager.delete_process = Mock(return_value=True)
    
    # Cria mock do AIService
    ai_service = Mock(spec=AIService)
    
    # Configura o resolve para retornar os mocks apropriados
    container.resolve.side_effect = lambda cls: {
        ProcessManager: process_manager,
        AIService: ai_service
    }[cls]
    
    return container

def test_controller_initialization(mock_container):
    """Testa inicialização do controller."""
    controller = ProcessController(mock_container)
    assert controller.container is mock_container
    assert isinstance(controller.process_manager, Mock)
    assert isinstance(controller.ai_service, Mock)

def test_create_process_success(mock_container):
    """Testa criação de processo com sucesso."""
    controller = ProcessController(mock_container)
    controller.process_manager.create_process.return_value = True
    
    result = controller.create_process({"name": "Test"})
    
    assert result == True
    controller.process_manager.create_process.assert_called_once_with({"name": "Test"})

def test_create_process_error(mock_container):
    """Testa erro na criação de processo."""
    controller = ProcessController(mock_container)
    controller.process_manager.create_process.side_effect = Exception("Error")
    
    result = controller.create_process({"name": "Test"})
    
    assert result == False

def test_update_process_success(mock_container):
    """Testa atualização de processo com sucesso."""
    controller = ProcessController(mock_container)
    controller.process_manager.update_process.return_value = True
    
    result = controller.update_process("123", {"name": "Updated"})
    
    assert result == True
    controller.process_manager.update_process.assert_called_once_with("123", {"name": "Updated"})

def test_get_process_success(mock_container):
    """Testa obtenção de processo com sucesso."""
    controller = ProcessController(mock_container)
    expected = {"id": "123", "name": "Test"}
    controller.process_manager.get_process.return_value = expected
    
    result = controller.get_process("123")
    
    assert result == expected
    controller.process_manager.get_process.assert_called_once_with("123")

def test_delete_process_success(mock_container):
    """Testa remoção de processo com sucesso."""
    controller = ProcessController(mock_container)
    controller.process_manager.delete_process.return_value = True
    
    result = controller.delete_process("123")
    
    assert result == True
    controller.process_manager.delete_process.assert_called_once_with("123") 