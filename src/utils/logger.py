"""Módulo de logging da aplicação."""
import logging
from typing import Optional

class Logger:
    """Logger customizado da aplicação."""
    
    def __init__(self, name: Optional[str] = None):
        """Inicializa o logger."""
        self.logger = logging.getLogger(name or __name__)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Configura o logger."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def info(self, message: str) -> None:
        """Registra mensagem de informação."""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Registra mensagem de erro."""
        self.logger.error(message)
    
    def warning(self, message: str) -> None:
        """Registra mensagem de aviso."""
        self.logger.warning(message)

# Exporta apenas a classe
__all__ = ['Logger'] 