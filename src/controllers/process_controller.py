"""Controlador de processos."""
from typing import Dict, Any, Optional
from managers.process_manager import ProcessManager
from utils.container_interface import ContainerInterface

class ProcessController:
    """Controlador para operações de processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o controlador.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        if container:
            self.manager = container.resolve(ProcessManager)
        else:
            self.manager = ProcessManager()
    
    def create_process(self, data: Dict[str, Any]) -> bool:
        """
        Cria um novo processo.
        
        Args:
            data: Dados do processo
            
        Returns:
            bool: True se criado com sucesso, False caso contrário
        """
        try:
            return self.manager.create_process(data)
        except Exception as e:
            print(f"Erro ao criar processo: {str(e)}")
            return False
    
    def update_process(self, process_id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza um processo existente.
        
        Args:
            process_id: ID do processo
            data: Novos dados
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            return self.manager.update_process(process_id, data)
        except Exception as e:
            print(f"Erro ao atualizar processo: {str(e)}")
            return False
    
    def delete_process(self, process_id: str) -> bool:
        """
        Exclui um processo.
        
        Args:
            process_id: ID do processo
            
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            return self.manager.delete_process(process_id)
        except Exception as e:
            print(f"Erro ao excluir processo: {str(e)}")
            return False 