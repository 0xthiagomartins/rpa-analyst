from typing import Dict
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
        self.output_dir = self._ensure_output_dir()
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _ensure_output_dir(self) -> str:
        """Garante que o diretório de saída existe."""
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def _create_custom_styles(self):
        """Cria estilos customizados para o documento."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Centralizado
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        ))
    
    def _validate_data(self, data: Dict) -> None:
        """Valida os dados necessários para gerar o PDD."""
        missing_fields = [field for field in self.REQUIRED_FIELDS if not data.get(field)]
        if missing_fields:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing_fields)}")
    
    def _create_field(self, label: str, value: str) -> Table:
        """Cria uma tabela para um campo do documento."""
        return Table(
            [[Paragraph(label, self.styles['Heading4']), 
              Paragraph(value, self.styles['Normal'])]],
            colWidths=[150, 350],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ])
        )
    
    def generate_pdd(self, data: Dict) -> str:
        """Gera o documento PDD em PDF."""
        try:
            # Valida os dados
            self._validate_data(data)
            
            # Define nome do arquivo
            process_name = data['process_name'].replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"PDD_{process_name}_{timestamp}.pdf"
            pdf_path = os.path.join(self.output_dir, filename)
            
            # Cria o documento
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            
            # Título
            elements.append(Paragraph("Process Definition Document (PDD)", self.styles['CustomTitle']))
            elements.append(Paragraph(data['process_name'], self.styles['Title']))
            elements.append(Spacer(1, 20))
            
            # Seções
            sections = [
                ("1. Identificação", [
                    ("Responsável:", data['process_owner']),
                    ("Descrição:", data['process_description'])
                ]),
                ("2. Detalhes do Processo", [
                    ("Passos do Processo:", data['steps_as_is']),
                    ("Sistemas/Ferramentas:", data['systems']),
                    ("Dados Utilizados:", data['data_used'])
                ]),
                ("3. Regras e Exceções", [
                    ("Regras de Negócio:", data['business_rules']),
                    ("Exceções:", data['exceptions'])
                ]),
                ("4. Automação", [
                    ("Objetivos:", data['automation_goals']),
                    ("KPIs:", data['kpis'])
                ])
            ]
            
            # Adiciona cada seção
            for title, fields in sections:
                elements.append(Paragraph(title, self.styles['SectionTitle']))
                for label, value in fields:
                    elements.append(self._create_field(label, value))
                    elements.append(Spacer(1, 10))
                elements.append(Spacer(1, 20))
            
            # Rodapé
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(
                f"Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                self.styles['Italic']
            ))
            
            # Gera o PDF
            doc.build(elements)
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDD: {str(e)}")
            raise ValueError(f"Erro ao gerar documento: {str(e)}") 