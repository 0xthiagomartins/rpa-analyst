"""Módulo de validação de formulários."""
from typing import Dict, Any, List
from utils.logger import Logger

class FormValidator:
    """Validador de formulários."""
    
    def __init__(self):
        """Inicializa o validador."""
        self.logger = Logger()
        self.errors: List[str] = []
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Valida os dados do formulário.
        
        Args:
            data: Dados para validar
            
        Returns:
            bool: True se válido, False caso contrário
        """
        self.errors = []
        
        try:
            # Validações básicas
            if not data:
                self.errors.append("Dados não fornecidos")
                return False
                
            # Campos obrigatórios
            required_fields = ["process_name", "process_owner"]
            for field in required_fields:
                if not data.get(field):
                    self.errors.append(f"Campo {field} é obrigatório")
            
            # Retorna True se não houver erros
            return len(self.errors) == 0
            
        except Exception as e:
            self.logger.error(f"Erro na validação: {str(e)}")
            self.errors.append("Erro interno na validação")
            return False
    
    def get_errors(self) -> List[str]:
        """
        Retorna a lista de erros.
        
        Returns:
            List[str]: Lista de mensagens de erro
        """
        return self.errors