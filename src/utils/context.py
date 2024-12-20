from src.utils.config import Config

class AppContext:
    """Classe para gerenciar o contexto global da aplicação."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = Config()
        return cls._instance
    
    @classmethod
    def get_config(cls) -> Config:
        """Retorna a instância de configuração."""
        return cls().config 