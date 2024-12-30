"""Módulo para logging específico da migração."""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

class MigrationLogger:
    """Logger específico para o processo de migração."""
    
    def __init__(self, log_dir: str = "logs/migration"):
        """
        Inicializa o logger.
        
        Args:
            log_dir: Diretório para armazenar logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configura logger
        self.logger = logging.getLogger("migration")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para arquivo
        log_file = self.log_dir / f"migration_{datetime.now():%Y%m%d_%H%M%S}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        """Registra mensagem de info."""
        self.logger.info(message)
    
    def error(self, message: str, error: Optional[Exception] = None) -> None:
        """Registra erro."""
        self.logger.error(message, exc_info=error)
    
    def warning(self, message: str) -> None:
        """Registra warning."""
        self.logger.warning(message)
    
    def debug(self, message: str) -> None:
        """Registra mensagem de debug."""
        self.logger.debug(message) 