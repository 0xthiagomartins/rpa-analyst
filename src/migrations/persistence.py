"""Módulo para persistência dos dados migrados."""
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime
import os

class MigrationPersistence:
    """Classe responsável pela persistência dos dados migrados."""
    
    def __init__(self, storage_path: str = "data/migrations"):
        """
        Inicializa o serviço de persistência.
        
        Args:
            storage_path: Caminho para armazenamento dos dados
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def save_identification_form(self, data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """
        Salva dados do IdentificationForm.
        
        Args:
            data: Dados a serem salvos
            process_id: ID do processo
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # Cria pasta do processo se não existir
            process_path = self.storage_path / process_id
            process_path.mkdir(exist_ok=True)
            
            # Salva dados em arquivo JSON
            file_path = process_path / "identification.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "data": data,
                    "metadata": {
                        "version": "1.0",
                        "migrated_at": datetime.now().isoformat(),
                        "status": "migrated"
                    }
                }, f, indent=2)
            
            self.logger.info(f"Saved identification data for process {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to save identification data: {str(e)}")
            raise
    
    def load_identification_form(self, process_id: str) -> Optional[Dict[str, Any]]:
        """
        Carrega dados do IdentificationForm.
        
        Args:
            process_id: ID do processo
            
        Returns:
            Dict com dados ou None se não encontrado
        """
        try:
            file_path = self.storage_path / process_id / "identification.json"
            if not file_path.exists():
                return None
                
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Failed to load identification data: {str(e)}")
            raise
    
    def delete_identification_form(self, process_id: str) -> Dict[str, Any]:
        """
        Remove dados do IdentificationForm.
        
        Args:
            process_id: ID do processo
            
        Returns:
            Dict com resultado da operação
        """
        try:
            file_path = self.storage_path / process_id / "identification.json"
            if file_path.exists():
                file_path.unlink()
                
            self.logger.info(f"Deleted identification data for process {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to delete identification data: {str(e)}")
            raise 

    def save_process_details_form(self, data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Salva dados do ProcessDetailsForm."""
        try:
            process_path = self.storage_path / process_id
            process_path.mkdir(exist_ok=True)
            
            file_path = process_path / "process_details.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "data": data,
                    "metadata": {
                        "version": "1.0",
                        "migrated_at": datetime.now().isoformat(),
                        "status": "migrated"
                    }
                }, f, indent=2)
            
            self.logger.info(f"Saved process details for {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to save process details: {str(e)}")
            raise

    def save_business_rules_form(self, data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Salva dados do BusinessRulesForm."""
        try:
            process_path = self.storage_path / process_id
            process_path.mkdir(exist_ok=True)
            
            file_path = process_path / "business_rules.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "data": data,
                    "metadata": {
                        "version": "1.0",
                        "migrated_at": datetime.now().isoformat(),
                        "status": "migrated"
                    }
                }, f, indent=2)
            
            self.logger.info(f"Saved business rules for {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to save business rules: {str(e)}")
            raise

    def save_automation_goals_form(self, data: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Salva dados do AutomationGoalsForm."""
        try:
            process_path = self.storage_path / process_id
            process_path.mkdir(exist_ok=True)
            
            file_path = process_path / "automation_goals.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "data": data,
                    "metadata": {
                        "version": "1.0",
                        "migrated_at": datetime.now().isoformat(),
                        "status": "migrated"
                    }
                }, f, indent=2)
            
            self.logger.info(f"Saved automation goals for {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to save automation goals: {str(e)}")
            raise

    # Métodos de carregamento
    def load_process_details_form(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Carrega dados do ProcessDetailsForm."""
        return self._load_form(process_id, "process_details.json")

    def load_business_rules_form(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Carrega dados do BusinessRulesForm."""
        return self._load_form(process_id, "business_rules.json")

    def load_automation_goals_form(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Carrega dados do AutomationGoalsForm."""
        return self._load_form(process_id, "automation_goals.json")

    # Métodos de deleção
    def delete_process_details_form(self, process_id: str) -> Dict[str, Any]:
        """Remove dados do ProcessDetailsForm."""
        return self._delete_form(process_id, "process_details.json")

    def delete_business_rules_form(self, process_id: str) -> Dict[str, Any]:
        """Remove dados do BusinessRulesForm."""
        return self._delete_form(process_id, "business_rules.json")

    def delete_automation_goals_form(self, process_id: str) -> Dict[str, Any]:
        """Remove dados do AutomationGoalsForm."""
        return self._delete_form(process_id, "automation_goals.json")

    # Métodos auxiliares
    def _load_form(self, process_id: str, filename: str) -> Optional[Dict[str, Any]]:
        """Método genérico para carregar formulários."""
        try:
            file_path = self.storage_path / process_id / filename
            if not file_path.exists():
                return None
                
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Failed to load {filename}: {str(e)}")
            raise

    def _delete_form(self, process_id: str, filename: str) -> Dict[str, Any]:
        """Método genérico para deletar formulários."""
        try:
            file_path = self.storage_path / process_id / filename
            if file_path.exists():
                file_path.unlink()
                
            self.logger.info(f"Deleted {filename} for process {process_id}")
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to delete {filename}: {str(e)}")
            raise 

    def save_data_form(self, data: Dict[str, Any], process_id: str) -> None:
        """Salva dados do DataForm."""
        try:
            self.logger.info(f"Saving DataForm data for process {process_id}")
            
            # Cria diretório se não existir
            process_dir = os.path.join(self.storage_path, process_id)
            os.makedirs(process_dir, exist_ok=True)
            
            # Salva arquivo
            file_path = os.path.join(process_dir, "data_form.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            self.logger.info("DataForm data saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save DataForm data: {str(e)}")
            raise

    def save_steps_form(self, data: Dict[str, Any], process_id: str) -> None:
        """Salva dados do StepsForm."""
        try:
            self.logger.info(f"Saving StepsForm data for process {process_id}")
            
            # Cria diretório se não existir
            process_dir = os.path.join(self.storage_path, process_id)
            os.makedirs(process_dir, exist_ok=True)
            
            # Salva arquivo
            file_path = os.path.join(process_dir, "steps_form.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            self.logger.info("StepsForm data saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save StepsForm data: {str(e)}")
            raise

    def delete_data_form(self, process_id: str) -> Dict[str, Any]:
        """Remove dados do DataForm."""
        try:
            self.logger.info(f"Deleting DataForm data for process {process_id}")
            
            file_path = os.path.join(self.storage_path, process_id, "data_form.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return {"success": True, "message": "DataForm data deleted successfully"}
        except Exception as e:
            self.logger.error(f"Failed to delete DataForm data: {str(e)}")
            return {"success": False, "message": str(e)}

    def delete_steps_form(self, process_id: str) -> Dict[str, Any]:
        """Remove dados do StepsForm."""
        try:
            self.logger.info(f"Deleting StepsForm data for process {process_id}")
            
            file_path = os.path.join(self.storage_path, process_id, "steps_form.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return {"success": True, "message": "StepsForm data deleted successfully"}
        except Exception as e:
            self.logger.error(f"Failed to delete StepsForm data: {str(e)}")
            return {"success": False, "message": str(e)} 