from abc import ABC, abstractmethod
from typing import Dict, Any
import jinja2
import os

class BaseTemplate(ABC):
    """Classe base para templates."""
    
    def __init__(self, template_name: str):
        self.template_name = template_name
        self.env = self._create_environment()
    
    def _create_environment(self) -> jinja2.Environment:
        """Cria e configura o ambiente Jinja2."""
        template_path = os.path.join(os.path.dirname(__file__), 'files')
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    @abstractmethod
    def render(self, data: Dict[str, Any]) -> str:
        """Renderiza o template com os dados fornecidos."""
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Valida os dados necessários para o template."""
        pass 