import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Criar e configurar o logger
logger = logging.getLogger('rpa_analyst')

# Exportar o logger
__all__ = ['logger'] 