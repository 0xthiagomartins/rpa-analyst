import os
import tempfile
import requests
import base64
import urllib.parse
from pathlib import Path
from src.utils.logger import logger

class MermaidService:
    """Serviço para manipulação de diagramas Mermaid."""
    
    def __init__(self):
        self.mermaid_cli_url = "https://mermaid.ink/svg/"
        self.cache_dir = Path("cache/diagrams")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def mermaid_to_image(self, mermaid_code: str, output_format: str = "svg") -> str:
        """Converte código Mermaid em imagem usando mermaid.ink."""
        try:
            # Verifica cache primeiro
            cache_key = self._get_cache_key(mermaid_code)
            cache_file = self.cache_dir / f"{cache_key}.{output_format}"
            
            if cache_file.exists():
                logger.debug(f"Usando imagem em cache: {cache_file}")
                return str(cache_file)
            
            # Sanitiza e prepara o código
            sanitized_code = self._sanitize_mermaid_code(mermaid_code)
            
            # Codifica o diagrama para URL de forma segura
            encoded_diagram = base64.urlsafe_b64encode(
                sanitized_code.encode('utf-8')
            ).decode('utf-8').rstrip('=')
            
            # Gera URL para a imagem
            image_url = f"{self.mermaid_cli_url}{encoded_diagram}"
            logger.debug(f"URL gerada: {image_url}")
            
            # Faz o download da imagem com timeout e headers apropriados
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'image/svg+xml, image/*'
            }
            response = requests.get(
                image_url, 
                timeout=10,
                headers=headers,
                verify=True
            )
            response.raise_for_status()
            
            # Salva em cache
            with open(cache_file, 'wb') as f:
                f.write(response.content)
            
            return str(cache_file)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição HTTP: {str(e)}")
            logger.debug(f"URL tentada: {image_url}")
            logger.debug(f"Código Mermaid: {mermaid_code}")
            return None
        except Exception as e:
            logger.error(f"Erro ao converter diagrama Mermaid: {str(e)}")
            return None
    
    def _get_cache_key(self, mermaid_code: str) -> str:
        """Gera uma chave única para o diagrama."""
        import hashlib
        return hashlib.md5(mermaid_code.encode()).hexdigest()
    
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
            'ñ': 'n',
            '"': "'",
            '"': "'",
            '"': "'",
            ''': "'",
            ''': "'",
            '–': "-",
            '—': "-",
            '…': "...",
            '≤': "<=",
            '≥': ">=",
            '×': "x",
            '÷': "/"
        }
        
        for old, new in replacements.items():
            code = code.replace(old, new)
        
        # Escapa caracteres especiais do Mermaid
        code = code.replace('[', '&#91;').replace(']', '&#93;')
        code = code.replace('(', '&#40;').replace(')', '&#41;')
        code = code.replace('<', '&#60;').replace('>', '&#62;')
        
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