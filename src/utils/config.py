import yaml
from typing import Dict, List
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Config:
    """Classe para gerenciar configurações da aplicação."""
    
    def __init__(self):
        self.config = self._load_config()
        logger.debug(f"Configuração carregada: {self.config}")
    
    def _load_config(self) -> dict:
        """Carrega as configurações do arquivo yaml."""
        try:
            config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
            logger.debug(f"Tentando carregar configuração de: {config_path}")
            
            if not config_path.exists():
                logger.warning(f"Arquivo de configuração não encontrado em: {config_path}")
                return self._get_default_config()
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if not self._validate_config(config):
                    logger.warning("Configuração inválida, usando padrão")
                    return self._get_default_config()
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return self._get_default_config()
    
    def _validate_config(self, config: dict) -> bool:
        """Valida a estrutura da configuração."""
        required_keys = ['app', 'forms']
        if not all(key in config for key in required_keys):
            return False
        
        if 'validation' not in config['forms']:
            return False
        
        if 'required_fields' not in config['forms']['validation']:
            return False
        
        return True
    
    def _get_default_config(self) -> dict:
        """Retorna a configuração padrão."""
        return {
            'app': {
                'title': 'Agente Analista de RPA',
                'description': 'Assistente para criação de documentos PDD',
                'version': '1.0.0'
            },
            'forms': {
                'validation': {
                    'required_fields': {
                        'identification': [
                            'process_name',
                            'process_owner',
                            'process_description'
                        ],
                        'process_details': [
                            'steps_as_is',
                            'systems',
                            'data_used'
                        ],
                        'business_rules': [
                            'business_rules',
                            'exceptions'
                        ],
                        'automation_goals': [
                            'automation_goals',
                            'kpis'
                        ]
                    }
                },
                'labels': {
                    'process_name': 'Nome do Processo',
                    'process_owner': 'Responsável pelo Processo',
                    'process_description': 'Descrição do Processo',
                    'steps_as_is': 'Passos do Processo',
                    'systems': 'Sistemas/Ferramentas',
                    'data_used': 'Dados Utilizados',
                    'business_rules': 'Regras de Negócio',
                    'exceptions': 'Exceções',
                    'automation_goals': 'Objetivos da Automação',
                    'kpis': 'KPIs'
                }
            }
        }
    
    def get_required_fields(self, section: str) -> List[str]:
        """Retorna os campos obrigatórios para uma seção específica."""
        return self.config.get('forms', {}).get('validation', {}).get('required_fields', {}).get(section, [])
    
    def get_field_label(self, field: str) -> str:
        """Retorna o rótulo para um campo específico."""
        return self.config.get('forms', {}).get('labels', {}).get(field, field) 