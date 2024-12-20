from typing import Optional, Dict, Any
import pdfkit
import os
from datetime import datetime
from src.templates.pdd_template import PDDTemplate
from src.models.process import Process
import logging
import platform

logger = logging.getLogger(__name__)

class DocumentService:
    """Serviço para geração e gerenciamento de documentos."""
    
    def __init__(self):
        self.template = PDDTemplate()
        self.output_dir = self._ensure_output_dir()
        self.wkhtmltopdf = self._get_wkhtmltopdf_path()
    
    def _ensure_output_dir(self) -> str:
        """Garante que o diretório de saída existe."""
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def _get_wkhtmltopdf_path(self) -> Optional[str]:
        """Retorna o caminho do executável wkhtmltopdf."""
        if platform.system() == 'Windows':
            # Caminhos comuns no Windows
            paths = [
                r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
                r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        else:
            # No Linux/Mac, tenta encontrar no PATH
            try:
                import subprocess
                path = subprocess.check_output(['which', 'wkhtmltopdf']).decode().strip()
                if os.path.exists(path):
                    return path
            except:
                pass
        return None
    
    def generate_html(self, process: Process) -> str:
        """Gera o documento HTML do PDD."""
        try:
            return self.template.render(process.to_dict())
        except Exception as e:
            logger.error(f"Erro ao gerar HTML: {e}")
            raise ValueError(f"Erro ao gerar documento: {e}")
    
    def generate_pdf(self, process: Process) -> str:
        """Gera o documento PDF do PDD."""
        if not self.wkhtmltopdf:
            raise RuntimeError(
                "wkhtmltopdf não encontrado. Por favor, instale seguindo as instruções em: "
                "https://wkhtmltopdf.org/downloads.html"
            )
            
        try:
            html_content = self.generate_html(process)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = process.name.replace(' ', '_')
            filename = f"PDD_{safe_name}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            
            # Configurações do PDF
            options = {
                'page-size': 'A4',
                'margin-top': '20mm',
                'margin-right': '20mm',
                'margin-bottom': '20mm',
                'margin-left': '20mm',
                'encoding': 'UTF-8',
                'no-outline': None
            }
            
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf)
            pdfkit.from_string(html_content, output_path, options=options, configuration=config)
            logger.info(f"PDF gerado com sucesso: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            raise ValueError(f"Erro ao gerar PDF: {e}")
    
    def get_document_path(self, process_name: str) -> Optional[str]:
        """Retorna o caminho do último documento gerado para um processo."""
        try:
            safe_name = process_name.replace(' ', '_')
            files = [f for f in os.listdir(self.output_dir) 
                    if f.startswith(f"PDD_{safe_name}_") and f.endswith(".pdf")]
            if not files:
                return None
            return os.path.join(self.output_dir, sorted(files)[-1])
        except Exception as e:
            logger.error(f"Erro ao buscar documento: {e}")
            return None 