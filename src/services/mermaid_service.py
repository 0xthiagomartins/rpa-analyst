import os
import tempfile
import requests
import base64
import urllib.parse
from src.utils.logger import logger

class MermaidService:
    """Serviço para manipulação de diagramas Mermaid."""
    
    def __init__(self):
        self.mermaid_cli_url = "https://mermaid.ink/svg/"
    
    def mermaid_to_image(self, mermaid_code: str, output_format: str = "svg") -> str:
        """Converte código Mermaid em imagem usando mermaid.ink."""
        try:
            # Sanitiza o código Mermaid
            sanitized_code = self._sanitize_mermaid_code(mermaid_code)
            
            # Codifica o diagrama para URL de forma segura
            encoded_diagram = base64.urlsafe_b64encode(
                sanitized_code.encode('utf-8')
            ).decode('utf-8').rstrip('=')
            
            # Gera URL para a imagem
            image_url = f"{self.mermaid_cli_url}{encoded_diagram}"
            
            # Faz o download da imagem com timeout
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Cria arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmp:
                tmp.write(response.content)
                return tmp.name
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição HTTP: {str(e)}")
            logger.debug(f"URL tentada: {image_url}")
            return None
        except Exception as e:
            logger.error(f"Erro ao converter diagrama Mermaid: {str(e)}")
            return None
    
    def _sanitize_mermaid_code(self, code: str) -> str:
        """Sanitiza o código Mermaid para evitar problemas de codificação."""
        # Remove espaços extras e quebras de linha desnecessárias
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        code = '\n'.join(lines)
        
        # Substitui caracteres especiais por versões ASCII
        replacements = {
            'ç': 'c',
            'ã': 'a',
            'á': 'a',
            'à': 'a',
            'â': 'a',
            'é': 'e',
            'ê': 'e',
            'í': 'i',
            'ó': 'o',
            'ô': 'o',
            'õ': 'o',
            'ú': 'u',
            'ü': 'u',
            'ñ': 'n'
        }
        
        for old, new in replacements.items():
            code = code.replace(old, new)
        
        return code
    
    def validate_mermaid_syntax(self, mermaid_code: str) -> bool:
        """Valida a sintaxe do código Mermaid."""
        try:
            # Sanitiza o código antes de validar
            sanitized_code = self._sanitize_mermaid_code(mermaid_code)
            
            # Tenta gerar uma imagem de teste
            test_image = self.mermaid_to_image(sanitized_code)
            if test_image and os.path.exists(test_image):
                os.unlink(test_image)  # Remove arquivo de teste
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao validar sintaxe Mermaid: {str(e)}")
            return False 