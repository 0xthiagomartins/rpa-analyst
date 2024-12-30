"""Controller para gerenciamento de processos."""
from typing import Dict, Any, Optional
from src.managers.process_manager import ProcessManager
from src.services.ai_service import AIService
from src.utils.dependency_container import DependencyContainer

class ProcessController:
    """Controller para operações relacionadas a processos."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa o controller."""
        self.container = container or DependencyContainer()
        self.process_manager = self.container.resolve(ProcessManager)
        self.ai_service = self.container.resolve(AIService)
    
    def create_process(self, data: Dict[str, Any]) -> bool:
        """Cria um novo processo."""
        try:
            return self.process_manager.create_process(data)
        except Exception as e:
            print(f"Erro ao criar processo: {str(e)}")
            return False
    
    def update_process(self, process_id: str, data: Dict[str, Any]) -> bool:
        """Atualiza um processo existente."""
        try:
            return self.process_manager.update_process(process_id, data)
        except Exception as e:
            print(f"Erro ao atualizar processo: {str(e)}")
            return False
    
    def get_process(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Obtém os dados de um processo."""
        try:
            return self.process_manager.get_process(process_id)
        except Exception as e:
            print(f"Erro ao obter processo: {str(e)}")
            return None
    
    def delete_process(self, process_id: str) -> bool:
        """Remove um processo."""
        try:
            return self.process_manager.delete_process(process_id)
        except Exception as e:
            print(f"Erro ao deletar processo: {str(e)}")
            return False 