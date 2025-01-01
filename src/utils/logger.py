"""Módulo de logging da aplicação."""
import logging
from datetime import datetime

class Logger:
    """Logger básico da aplicação."""
    
    def __init__(self):
        """Inicializa o logger."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self._logger = logging.getLogger(__name__)
    
    def info(self, message: str) -> None:
        """Registra mensagem de informação."""
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """Registra mensagem de aviso."""
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """Registra mensagem de erro."""
        self._logger.error(message)
    
    def debug(self, message: str) -> None:
        """Registra mensagem de debug."""
        self._logger.debug(message)

# Exporta apenas a classe
__all__ = ['Logger'] 