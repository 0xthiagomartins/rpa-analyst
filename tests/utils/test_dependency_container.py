"""Testes para o container de dependências."""
import pytest
from src.utils.dependency_container import DependencyContainer
from src.services.ai_service import AIService
from src.services.mermaid_service import MermaidService
from src.managers.process_manager import ProcessManager
from src.utils.config import Config

class MockService:
    """Serviço mock para testes."""
    def __init__(self, name: str = "mock"):
        self.name = name

def test_container_initialization():
    """Testa inicialização do container."""
    container = DependencyContainer()
    assert isinstance(container._instances, dict)
    
    # Verifica se os serviços padrão foram registrados
    assert AIService in container._instances
    assert MermaidService in container._instances
    assert ProcessManager in container._instances
    assert Config in container._instances

def test_register_class():
    """Testa registro de uma classe."""
    container = DependencyContainer()
    container.register(MockService)
    assert MockService in container._instances
    assert container._instances[MockService] is None

def test_register_instance():
    """Testa registro de uma instância específica."""
    container = DependencyContainer()
    mock = MockService("test")
    container.register_instance(MockService, mock)
    assert container._instances[MockService] is mock

def test_resolve_registered_class():
    """Testa resolução de uma classe registrada."""
    container = DependencyContainer()
    container.register(MockService)
    
    instance = container.resolve(MockService)
    assert isinstance(instance, MockService)
    
    # Verifica se a mesma instância é retornada
    instance2 = container.resolve(MockService)
    assert instance is instance2

def test_resolve_registered_instance():
    """Testa resolução de uma instância registrada."""
    container = DependencyContainer()
    mock = MockService("test")
    container.register_instance(MockService, mock)
    
    resolved = container.resolve(MockService)
    assert resolved is mock

def test_resolve_unregistered():
    """Testa tentativa de resolver classe não registrada."""
    container = DependencyContainer()
    with pytest.raises(ValueError):
        container.resolve(MockService)

def test_default_services():
    """Testa se os serviços padrão são resolvidos corretamente."""
    container = DependencyContainer()
    
    ai_service = container.resolve(AIService)
    assert isinstance(ai_service, AIService)
    
    mermaid_service = container.resolve(MermaidService)
    assert isinstance(mermaid_service, MermaidService)
    
    process_manager = container.resolve(ProcessManager)
    assert isinstance(process_manager, ProcessManager)
    
    config = container.resolve(Config)
    assert isinstance(config, Config) 