from typing import Dict, Optional, List
from src.models.process import Process
from src.utils.validators import FormValidator
import logging

logger = logging.getLogger(__name__)

class ProcessManager:
    """Gerencia o ciclo de vida dos processos."""
    
    def __init__(self):
        self.processes: Dict[str, Process] = {}
        self.validator = FormValidator()
        self.current_process_id: Optional[str] = None
    
    def create_process(self, data: dict) -> Process:
        """
        Cria um novo processo com validações de negócio.
        
        Args:
            data: Dicionário com os dados do processo
            
        Returns:
            Process: Instância do processo criado
            
        Raises:
            ValidationError: Se os dados não passarem na validação
        """
        # Valida os dados antes de criar o processo
        errors = self.validator.validate_form(data, 'identification')
        if errors:
            error_messages = [f"{error.field}: {error.message}" for error in errors]
            raise ValueError(f"Dados inválidos: {', '.join(error_messages)}")
        
        process = Process.from_dict(data)
        self.processes[process.name] = process
        self.current_process_id = process.name
        
        logger.info(f"Processo criado: {process.name}")
        return process
    
    def update_process(self, process_name: str, data: dict) -> Process:
        """Atualiza um processo existente."""
        if process_name not in self.processes:
            raise KeyError(f"Processo não encontrado: {process_name}")
        
        process = self.processes[process_name]
        updated_data = process.to_dict()
        updated_data.update(data)
        
        # Valida os dados atualizados
        self._validate_update(updated_data)
        
        self.processes[process_name] = Process.from_dict(updated_data)
        logger.info(f"Processo atualizado: {process_name}")
        
        return self.processes[process_name]
    
    def get_process(self, process_name: str) -> Optional[Process]:
        """Retorna um processo pelo nome."""
        return self.processes.get(process_name)
    
    def get_current_process(self) -> Optional[Process]:
        """Retorna o processo atual."""
        if self.current_process_id:
            return self.processes.get(self.current_process_id)
        return None
    
    def list_processes(self) -> List[Process]:
        """Retorna lista de todos os processos."""
        return list(self.processes.values())
    
    def _validate_update(self, data: dict) -> None:
        """Valida dados de atualização baseado na etapa atual."""
        # Identifica qual seção está sendo atualizada
        sections = ['identification', 'process_details', 'business_rules', 'automation_goals']
        
        for section in sections:
            if any(key in data for key in self.validator.config.get_required_fields(section)):
                errors = self.validator.validate_form(data, section)
                if errors:
                    error_messages = [f"{error.field}: {error.message}" for error in errors]
                    raise ValueError(f"Dados inválidos para {section}: {', '.join(error_messages)}") 