from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Process:
    """Modelo de dados para um processo RPA."""
    
    # Identificação do Processo
    name: str
    owner: str
    description: str
    
    # Detalhes do Processo
    steps_as_is: str
    systems: str
    data_used: str
    
    # Regras e Exceções
    business_rules: str
    exceptions: str
    
    # Objetivos e KPIs
    automation_goals: str
    kpis: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Process':
        """Cria uma instância de Process a partir de um dicionário."""
        return cls(
            name=data.get('process_name', ''),
            owner=data.get('process_owner', ''),
            description=data.get('process_description', ''),
            steps_as_is=data.get('steps_as_is', ''),
            systems=data.get('systems', ''),
            data_used=data.get('data_used', ''),
            business_rules=data.get('business_rules', ''),
            exceptions=data.get('exceptions', ''),
            automation_goals=data.get('automation_goals', ''),
            kpis=data.get('kpis', '')
        )
    
    def to_dict(self) -> Dict[str, str]:
        """Converte a instância em um dicionário."""
        return {
            'process_name': self.name,
            'process_owner': self.owner,
            'process_description': self.description,
            'steps_as_is': self.steps_as_is,
            'systems': self.systems,
            'data_used': self.data_used,
            'business_rules': self.business_rules,
            'exceptions': self.exceptions,
            'automation_goals': self.automation_goals,
            'kpis': self.kpis
        } 