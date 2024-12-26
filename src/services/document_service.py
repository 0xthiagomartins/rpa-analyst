from typing import Dict, List
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.utils.logger import logger
from src.services.ai_service import AIService

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
    
    def validate_pdd_data(self, data: dict) -> bool:
        """Valida os dados necessários para gerar o PDD."""
        required_fields = [
            "process_name",
            "process_owner",
            "process_description",
            "steps_as_is",
            "systems",
            "data_used",
            "business_rules",
            "exceptions",
            "automation_goals",
            "kpis"
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing_fields)}")
        
        return True
    
    def _format_value(self, value) -> str:
        """Formata um valor para exibição no PDF."""
        if isinstance(value, list):
            return "\n• " + "\n• ".join(str(item) for item in value)
        elif isinstance(value, dict):
            return "\n".join(f"{k}: {self._format_value(v)}" for k, v in value.items())
        return str(value)
    
    def _create_field(self, label: str, value) -> Table:
        """Cria uma tabela para um campo do documento."""
        formatted_value = self._format_value(value)
        return Table(
            [[Paragraph(label, self.styles['Heading4']), 
              Paragraph(formatted_value, self.styles['Normal'])]],
            colWidths=[150, 350],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinha texto ao topo
            ])
        )
    
    def _create_list_field(self, items: List[str]) -> Table:
        """Cria uma tabela com itens em formato de lista."""
        formatted_items = "\n".join(f"• {item}" for item in items)
        return Table(
            [[Paragraph(formatted_items, self.styles['Normal'])]],
            colWidths=[500],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ])
        )
    
    def generate_pdd(self, data: dict) -> str:
        """Gera o documento PDD em PDF."""
        try:
            # Valida os dados
            self.validate_pdd_data(data)
            
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
            
            # Gera o diagrama
            ai_service = AIService()
            mermaid_code = ai_service.generate_process_diagram(data)
            
            # Adiciona o diagrama ao documento
            elements.append(Paragraph("2.1 Diagrama do Processo", self.styles['SectionTitle']))
            elements.append(Paragraph("O diagrama abaixo representa o fluxo do processo:", self.styles['Normal']))
            
            # TODO: Converter diagrama Mermaid para imagem e adicionar ao PDF
            # Por enquanto, adiciona como texto
            elements.append(Paragraph(mermaid_code, self.styles['Code']))
            
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