"""Configurações e opções para os formulários do processo."""
import yaml
from pathlib import Path
import streamlit as st

def get_default_options():
    """Retorna as opções padrão caso o arquivo de configuração não exista."""
    return {
        'common_tools': [
            'Microsoft Excel',
            'Microsoft Outlook',
            'SAP',
            'Power BI',
            'SharePoint',
            'Teams',
            'Oracle',
            'Salesforce',
            'ServiceNow',
            'Power Automate'
        ],
        'data_types': [
            'Dados financeiros',
            'Documentos fiscais',
            'Dados cadastrais',
            'Dados de controle',
            'Documentos digitalizados',
            'Planilhas',
            'Emails',
            'Relatórios',
            'Números de protocolo',
            'Valores monetários',
            'Dados de login',
            'Arquivos PDF'
        ],
        'data_formats': [
            'PDF',
            'Excel',
            'Word',
            'CSV',
            'TXT',
            'XML',
            'JSON',
            'Email',
            'Imagem',
            'Login',
            'Monetário'
        ],
        'data_sources': [
            'Email',
            'Sistema interno',
            'Portal web',
            'Pasta compartilhada',
            'Banco de dados',
            'API',
            'Planilha',
            'Scanner'
        ],
        'business_rules_templates': [
            'Validação de dados obrigatórios',
            'Verificação de duplicidade',
            'Aprovação por valor',
            'Verificação de prazo',
            'Validação de formato',
            'Checagem de permissões'
        ],
        'common_exceptions': [
            'Sistema indisponível',
            'Dados inconsistentes',
            'Arquivo corrompido',
            'Timeout de operação',
            'Erro de autenticação',
            'Permissão negada'
        ],
        'automation_goals': [
            'Redução de tempo de processamento',
            'Eliminação de erros manuais',
            'Padronização do processo',
            'Aumento de produtividade',
            'Melhoria da qualidade',
            'Redução de custos'
        ],
        'kpi_templates': [
            'Tempo médio de processamento',
            'Taxa de erro',
            'Volume processado',
            'Custo por transação',
            'Tempo de resposta',
            'Satisfação do usuário'
        ]
    }

def load_form_options():
    """Carrega as opções predefinidas do formulário."""
    try:
        # Usa str() para garantir que o Path seja convertido corretamente
        config_path = Path(str(Path(__file__).parent.parent.parent.parent.parent / 'config' / 'form_options.yaml'))
        if not config_path.exists():
            return get_default_options()
            
        with open(str(config_path), 'r', encoding='utf-8') as f:
            file_options = yaml.safe_load(f)
            
        # Se o arquivo existe mas está vazio ou inválido
        if not file_options or not isinstance(file_options, dict):
            return get_default_options()
            
        # Verifica se todas as chaves necessárias existem
        default_options = get_default_options()
        result = {}
        
        # Para cada chave nas opções padrão
        for key in default_options:
            # Se a chave existe no arquivo, usa o valor do arquivo
            if key in file_options:
                result[key] = file_options[key]
            # Se não existe, usa o valor padrão
            else:
                result[key] = default_options[key]
                
        return result
    except Exception as e:
        st.warning(f"Erro ao carregar opções do arquivo: {str(e)}. Usando opções padrão.")
        return get_default_options()

OPTIONS = load_form_options() 