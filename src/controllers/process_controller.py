from typing import Optional
from src.models.process import Process
from src.managers.process_manager import ProcessManager

class ProcessController:
    """Controlador para gerenciar processos RPA."""
    
    def __init__(self):
        self.process_manager = ProcessManager()
    
    def create_process(self, process_data: dict) -> Process:
        """Cria um novo processo a partir dos dados fornecidos."""
        return self.process_manager.create_process(process_data)
    
    def update_process(self, process_data: dict) -> Process:
        """Atualiza os dados do processo atual."""
        current = self.get_current_process()
        if not current:
            return self.create_process(process_data)
        
        return self.process_manager.update_process(current.name, process_data)
    
    def get_current_process(self) -> Optional[Process]:
        """Retorna o processo atual."""
        return self.process_manager.get_current_process() 