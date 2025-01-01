"""Interface base para injeção de dependências."""
from typing import Protocol, Type, Any

class ContainerInterface(Protocol):
    """Interface para containers de dependência."""
    
    def register(self, cls: Type, instance: Any = None) -> None:
        """Registra uma dependência."""
        ...
    
    def resolve(self, cls: Type) -> Any:
        """Resolve uma dependência."""
        ... 