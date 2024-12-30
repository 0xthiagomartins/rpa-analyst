"""Módulo para gerenciar backups durante a migração."""
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from src.utils.migration_logger import MigrationLogger

class BackupService:
    """Serviço para gerenciar backups dos dados durante a migração."""
    
    def __init__(self, backup_dir: str = "backups/migration"):
        """
        Inicializa o serviço de backup.
        
        Args:
            backup_dir: Diretório para armazenar backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logger = MigrationLogger()
    
    def create_backup(self, form_name: str, data: Dict[str, Any]) -> Optional[Path]:
        """
        Cria um backup dos dados de um formulário.
        
        Args:
            form_name: Nome do formulário
            data: Dados a serem backupeados
            
        Returns:
            Path: Caminho do arquivo de backup ou None se falhar
        """
        try:
            # Cria diretório específico para o formulário
            form_backup_dir = self.backup_dir / form_name
            form_backup_dir.mkdir(exist_ok=True)
            
            # Gera nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = form_backup_dir / f"backup_{timestamp}.json"
            
            # Salva dados
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.logger.log_info(f"Backup created for {form_name} at {backup_file}")
            return backup_file
            
        except Exception as e:
            self.logger.log_error(f"Error creating backup for {form_name}", e)
            return None
    
    def restore_backup(self, backup_file: Path) -> Optional[Dict[str, Any]]:
        """
        Restaura dados de um backup.
        
        Args:
            backup_file: Caminho do arquivo de backup
            
        Returns:
            Dict: Dados restaurados ou None se falhar
        """
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.log_info(f"Backup restored from {backup_file}")
            return data
            
        except Exception as e:
            self.logger.log_error(f"Error restoring backup from {backup_file}", e)
            return None
    
    def list_backups(self, form_name: Optional[str] = None) -> Dict[str, list]:
        """
        Lista backups disponíveis.
        
        Args:
            form_name: Nome do formulário (opcional)
            
        Returns:
            Dict: Dicionário com backups por formulário
        """
        backups = {}
        
        if form_name:
            form_dir = self.backup_dir / form_name
            if form_dir.exists():
                backups[form_name] = [f.name for f in form_dir.glob("backup_*.json")]
        else:
            for form_dir in self.backup_dir.iterdir():
                if form_dir.is_dir():
                    backups[form_dir.name] = [
                        f.name for f in form_dir.glob("backup_*.json")
                    ]
        
        return backups
    
    def cleanup_old_backups(self, max_backups: int = 5) -> None:
        """
        Remove backups antigos mantendo apenas os N mais recentes.
        
        Args:
            max_backups: Número máximo de backups a manter por formulário
        """
        for form_dir in self.backup_dir.iterdir():
            if form_dir.is_dir():
                backups = sorted(
                    form_dir.glob("backup_*.json"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )
                
                # Remove backups excedentes
                for backup in backups[max_backups:]:
                    backup.unlink()
                    self.logger.log_info(f"Removed old backup: {backup}") 