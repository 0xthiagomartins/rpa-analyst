from typing import Dict, List
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.utils.logger import logger
from src.services.ai_service import AIService
from reportlab.lib.utils import ImageReader
import tempfile
import json
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

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
        # Estilo do título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#2C3E50')
        ))
        
        # Estilo para seções
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=15,
            textColor=colors.HexColor('#34495E'),
            borderPadding=(0, 0, 2, 0),  # padding inferior
            borderWidth=1,
            borderColor=colors.HexColor('#BDC3C7')
        ))
        
        # Estilo para subseções
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#7F8C8D')
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            spaceAfter=8
        ))
        
        # Estilo para itens de lista
        self.styles.add(ParagraphStyle(
            name='ListItem',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            leftIndent=20,
            bulletIndent=10
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
    
    def _create_header(self, canvas, doc):
        """Cria o cabeçalho do documento."""
        canvas.saveState()
        # Linha superior
        canvas.setStrokeColor(colors.HexColor('#3498DB'))
        canvas.setLineWidth(2)
        canvas.line(40, doc.pagesize[1] - 40, doc.pagesize[0] - 40, doc.pagesize[1] - 40)
        
        # Logo ou texto do cabeçalho
        canvas.setFillColor(colors.HexColor('#2C3E50'))
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(50, doc.pagesize[1] - 35, "Process Definition Document (PDD)")
        
        # Data no canto direito
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(
            doc.pagesize[0] - 50, 
            doc.pagesize[1] - 35,
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Cria o rodapé do documento."""
        canvas.saveState()
        # Linha inferior
        canvas.setStrokeColor(colors.HexColor('#3498DB'))
        canvas.setLineWidth(1)
        canvas.line(40, 50, doc.pagesize[0] - 40, 50)
        
        # Número da página
        canvas.setFont("Helvetica", 8)
        page_num = canvas.getPageNumber()
        canvas.drawRightString(
            doc.pagesize[0] - 50,
            35,
            f"Página {page_num}"
        )
        canvas.restoreState()
    
    def _create_info_box(self, label: str, value, background_color: str = '#F8F9FA') -> Table:
        """Cria uma caixa de informação estilizada."""
        return Table(
            [[Paragraph(label, self.styles['SubSection']), 
              Paragraph(self._format_value(value), self.styles['CustomBody'])]],
            colWidths=[150, 350],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(background_color)),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E9ECEF')),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#495057')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
            ])
        )
    
    def _create_section(self, title: str, content_list: list) -> list:
        """Cria uma seção com título e lista de conteúdo."""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionTitle']))
        
        for item in content_list:
            elements.append(
                Paragraph(f"• {item}", self.styles['ListItem'])
            )
        elements.append(Spacer(1, 10))
        return elements
    
    def _mermaid_to_image(self, mermaid_code: str) -> str:
        """Converte código Mermaid em imagem PNG usando Mermaid Live Editor API."""
        try:
            # Usa a API do Mermaid Live Editor para gerar SVG
            response = requests.post(
                'https://mermaid.live/api/v1/svg',
                json={'code': mermaid_code}
            )
            
            if response.status_code == 200:
                svg_content = response.text
                
                # Arquivos temporários
                svg_file = os.path.join(tempfile.gettempdir(), 'diagram.svg')
                png_file = os.path.join(tempfile.gettempdir(), 'diagram.png')
                
                # Salva o SVG em arquivo
                with open(svg_file, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                # Converte SVG para PNG usando svglib
                drawing = svg2rlg(svg_file)
                renderPM.drawToFile(drawing, png_file, fmt='PNG')
                
                # Remove arquivo SVG temporário
                os.unlink(svg_file)
                
                return png_file
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao converter diagrama: {str(e)}")
            return None

    def _add_diagram_section(self, elements: list, mermaid_code: str):
        """Adiciona seção do diagrama ao documento."""
        elements.append(Paragraph("Diagrama do Processo", self.styles['SectionTitle']))
        elements.append(Spacer(1, 10))
        
        try:
            # Converte diagrama em imagem
            img_path = self._mermaid_to_image(mermaid_code)
            if img_path and os.path.exists(img_path):
                # Adiciona a imagem ao PDF
                img = ImageReader(img_path)
                img_width = 500  # Largura máxima da imagem
                aspect = img.getSize()[1] / img.getSize()[0]
                img_height = img_width * aspect
                
                elements.append(Image(img_path, width=img_width, height=img_height))
                elements.append(Spacer(1, 20))
                
                # Remove arquivo temporário
                os.unlink(img_path)
            else:
                elements.append(Paragraph(
                    "Não foi possível gerar o diagrama.",
                    self.styles['CustomBody']
                ))
        except Exception as e:
            logger.error(f"Erro ao adicionar diagrama: {str(e)}")
            elements.append(Paragraph(
                "Erro ao gerar diagrama do processo.",
                self.styles['CustomBody']
            ))

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
            
            # Cria o documento com cabeçalho e rodapé
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                rightMargin=50,
                leftMargin=50,
                topMargin=60,
                bottomMargin=60
            )
            
            # Lista de elementos do documento
            elements = []
            
            # Título e subtítulo
            elements.append(Paragraph(data['process_name'], self.styles['CustomTitle']))
            elements.append(Spacer(1, 20))
            
            # Informações básicas
            elements.append(self._create_info_box(
                "Responsável:",
                data['process_owner'],
                '#EBF5FB'
            ))
            elements.append(Spacer(1, 10))
            elements.append(self._create_info_box(
                "Descrição:",
                data['process_description'],
                '#EBF5FB'
            ))
            elements.append(Spacer(1, 20))
            
            # Seções principais
            elements.extend(self._create_section(
                "Etapas do Processo",
                data['steps_as_is']
            ))
            
            elements.extend(self._create_section(
                "Sistemas e Ferramentas",
                data['systems']
            ))
            
            # Dados utilizados
            elements.append(Paragraph("Dados do Processo", self.styles['SectionTitle']))
            for key, value in data['data_used'].items():
                elements.append(self._create_info_box(
                    f"{key.title()}:",
                    value,
                    '#F4F6F6'
                ))
                elements.append(Spacer(1, 5))
            
            # Regras e exceções
            elements.extend(self._create_section(
                "Regras de Negócio",
                data['business_rules']
            ))
            
            elements.extend(self._create_section(
                "Exceções",
                data['exceptions']
            ))
            
            # Objetivos e KPIs
            elements.extend(self._create_section(
                "Objetivos da Automação",
                data['automation_goals']
            ))
            
            elements.extend(self._create_section(
                "KPIs",
                data['kpis']
            ))
            
            # Adiciona o diagrama antes dos KPIs
            if 'diagram_code' in data:
                self._add_diagram_section(elements, data['diagram_code'])
            
            # Gera o PDF
            doc.build(
                elements,
                onFirstPage=self._create_header,
                onLaterPages=self._create_footer
            )
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDD: {str(e)}")
            raise ValueError(f"Erro ao gerar documento: {str(e)}") 