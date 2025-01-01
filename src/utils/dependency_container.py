"""Módulo para gerenciamento de dependências."""
from typing import Type, Any, Dict, Optional
from utils.container_interface import ContainerInterface
from utils.logger import Logger

class DependencyContainer(ContainerInterface):
    """Container de dependências da aplicação."""
    
    def __init__(self):
        """Inicializa o container."""
        self._services: Dict[Type, Any] = {}
        self._register_defaults()
    
    def _register_defaults(self) -> None:
        """Registra as dependências padrão."""
        # Registra serviços básicos
        self.register(Logger)
        
        # Registra StateManager (lazy loading)
        from views.components.state.state_manager import StateManager
        self.register(StateManager)
        
        # Importa e registra outros componentes
        from controllers.process_controller import ProcessController
        from managers.process_manager import ProcessManager
        
        # Tenta registrar serviços opcionais
        self._try_register_service('services.document_service', 'DocumentService')
        
        # Registra managers
        self.register(ProcessManager)
        
        # Registra controllers
        self.register(ProcessController)
    
    def _try_register_service(self, module_path: str, class_name: str) -> None:
        """Tenta registrar um serviço opcional."""
        try:
            module = __import__(module_path, fromlist=[class_name])
            service_class = getattr(module, class_name)
            self.register(service_class)
        except (ImportError, AttributeError) as e:
            self.logger.warning(f"Serviço {class_name} não disponível: {str(e)}")
    
    @property
    def logger(self) -> Logger:
        """Obtém o logger."""
        if Logger not in self._services:
            self.register(Logger)
        return self._services[Logger]
    
    def register(self, cls: Type, instance: Any = None) -> None:
        """
        Registra uma dependência no container.
        
        Args:
            cls: Classe da dependência
            instance: Instância opcional da dependência
        """
        if instance is None:
            try:
                instance = cls(self)
            except TypeError:
                instance = cls()
        
        self._services[cls] = instance
    
    def resolve(self, cls: Type) -> Any:
        """
        Resolve uma dependência.
        
        Args:
            cls: Classe da dependência
            
        Returns:
            Instância da dependência
            
        Raises:
            ValueError: Se a dependência não estiver registrada
        """
        if cls not in self._services:
            raise ValueError(f"Dependência não registrada: {cls}")
        return self._services[cls] 