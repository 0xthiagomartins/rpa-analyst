from typing import Dict
import jinja2
import os
from datetime import datetime
from weasyprint import HTML
from src.utils.logger import logger

class DocumentService:
    """Serviço para geração de documentos PDD."""
    
    REQUIRED_FIELDS = [
        'process_name',
        'process_owner',
        'process_description',
        'steps_as_is',
        'systems',
        'data_used',
        'business_rules',
        'exceptions',
        'automation_goals',
        'kpis'
    ]
    
    def __init__(self):
        self.template_env = self._create_template_env()
        self.output_dir = self._ensure_output_dir()
    
    def _create_template_env(self) -> jinja2.Environment:
        """Cria ambiente Jinja2 para templates."""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'files')
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            autoescape=True
        )
    
    def _ensure_output_dir(self) -> str:
        """Garante que o diretório de saída existe."""
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def _validate_data(self, data: Dict) -> None:
        """Valida os dados necessários para gerar o PDD."""
        missing_fields = [field for field in self.REQUIRED_FIELDS if not data.get(field)]
        if missing_fields:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing_fields)}")
    
    def generate_pdd(self, data: Dict) -> str:
        """Gera o documento PDD em HTML e PDF."""
        try:
            # Valida os dados
            self._validate_data(data)
            
            # Carrega o template
            template = self.template_env.get_template('pdd.html')
            
            # Adiciona data de geração
            data['generated_at'] = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Gera HTML
            html_content = template.render(**data)
            
            # Define nomes dos arquivos
            process_name = data['process_name'].replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"PDD_{process_name}_{timestamp}"
            
            html_path = os.path.join(self.output_dir, f"{filename}.html")
            pdf_path = os.path.join(self.output_dir, f"{filename}.pdf")
            
            # Salva HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Converte para PDF usando WeasyPrint
            HTML(string=html_content).write_pdf(pdf_path)
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDD: {str(e)}")
            raise ValueError(f"Erro ao gerar documento: {str(e)}") 