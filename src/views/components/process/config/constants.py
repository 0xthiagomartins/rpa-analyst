"""Constantes para o módulo de processo."""
from src.utils.config_constants import UI_CONFIG

ERROR_MESSAGES = {
    'REQUIRED_FIELD': '❌ Todos os campos obrigatórios devem ser preenchidos',
    'INVALID_FORMAT': '❌ Formato inválido',
    'SAVE_ERROR': '❌ Erro ao salvar os dados'
}

# Re-exporta UI_CONFIG para manter compatibilidade
__all__ = ['ERROR_MESSAGES', 'UI_CONFIG'] 