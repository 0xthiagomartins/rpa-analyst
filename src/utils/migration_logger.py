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
    
    def start_migration(self, form_name: str) -> None:
        """Registra início da migração de um formulário."""
        self.logger.info(f"Starting migration for {form_name}")
    
    def end_migration(self, form_name: str, success: bool) -> None:
        """Registra fim da migração de um formulário."""
        status = "successfully" if success else "with errors"
        self.logger.info(f"Migration for {form_name} finished {status}")
    
    def log_error(self, form_name: str, error: Exception, data: Optional[dict] = None) -> None:
        """Registra erro durante migração."""
        self.logger.error(
            f"Error migrating {form_name}: {str(error)}",
            exc_info=True,
            extra={"data": data} if data else None
        )
    
    def log_warning(self, form_name: str, message: str) -> None:
        """Registra warning durante migração."""
        self.logger.warning(f"{form_name}: {message}")
    
    def log_data_migration(self, form_name: str, old_data: dict, new_data: dict) -> None:
        """Registra detalhes da migração de dados."""
        self.logger.debug(
            f"Data migration for {form_name}:\n"
            f"Old data: {old_data}\n"
            f"New data: {new_data}"
        ) 