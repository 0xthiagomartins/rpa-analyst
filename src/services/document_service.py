"""Serviço para geração de documentos."""
from typing import Dict, Any, Optional
import os
import json
from utils.logger import Logger

class DocumentService:
    """Serviço para geração e manipulação de documentos."""
    
    def __init__(self):
        """Inicializa o serviço."""
        self.logger = Logger()
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'output'
        )
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdd(self, data: Dict[str, Any], output_path: Optional[str] = None) -> bool:
        """
        Gera um PDD (Process Design Document) em formato JSON.
        
        Args:
            data: Dados do processo
            output_path: Caminho para salvar o arquivo
            
        Returns:
            bool: True se gerado com sucesso, False caso contrário
        """
        try:
            # Define caminho de saída
            if not output_path:
                output_path = os.path.join(
                    self.output_dir,
                    f"pdd_{data.get('process_id', 'unknown')}.json"
                )
            
            # Salva como JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"PDD gerado com sucesso: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar PDD: {str(e)}")
            return False
    
    def save_diagram(self, diagram_code: str, output_path: str) -> bool:
        """
        Salva um diagrama em arquivo.
        
        Args:
            diagram_code: Código do diagrama
            output_path: Caminho para salvar
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(diagram_code)
            
            self.logger.info(f"Diagrama salvo em: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar diagrama: {str(e)}")
            return False 