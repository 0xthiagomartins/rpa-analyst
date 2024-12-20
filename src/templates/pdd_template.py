from typing import Dict, Any
from .base_template import BaseTemplate

class PDDTemplate(BaseTemplate):
    """Template para geração de PDD."""
    
    def __init__(self):
        super().__init__('pdd.html')
        
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Valida os dados necessários para o PDD."""
        required_fields = [
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
        return all(field in data and data[field] for field in required_fields)
    
    def render(self, data: Dict[str, Any]) -> str:
        """Renderiza o PDD com os dados fornecidos."""
        if not self.validate_data(data):
            raise ValueError("Dados incompletos para geração do PDD")
        
        template = self.env.get_template(self.template_name)
        return template.render(**data) 