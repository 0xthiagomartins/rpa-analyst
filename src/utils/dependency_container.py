"""Módulo para gerenciamento de dependências."""
from typing import Dict, Type, Any
from src.services.ai_service import AIService
from src.services.mermaid_service import MermaidService
from src.managers.process_manager import ProcessManager
from src.utils.config import Config

class DependencyContainer:
    """Container para gerenciar dependências da aplicação."""
    
    def __init__(self):
        """Inicializa o container."""
        self._instances: Dict[Type, Any] = {}
        self._register_defaults()
    
    def _register_defaults(self) -> None:
        """Registra as dependências padrão."""
        # Serviços
        self.register(AIService)
        self.register(MermaidService)
        
        # Configuração
        config = Config()
        self.register_instance(Config, config)
        
        # Managers
        self.register(ProcessManager)
    
    def register(self, cls: Type) -> None:
        """Registra uma classe no container."""
        self._instances[cls] = None
    
    def register_instance(self, cls: Type, instance: Any) -> None:
        """Registra uma instância específica."""
        self._instances[cls] = instance
    
    def resolve(self, cls: Type) -> Any:
        """Resolve uma dependência."""
        if cls not in self._instances:
            raise ValueError(f"Dependência não registrada: {cls}")
            
        instance = self._instances[cls]
        if instance is None:
            instance = cls()
            self._instances[cls] = instance
            
        return instance 