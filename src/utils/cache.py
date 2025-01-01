"""Módulo de cache em memória."""
from typing import Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict

class InMemoryCache:
    """
    Cache em memória com interface similar ao Redis.
    Implementa LRU (Least Recently Used) para gerenciamento de memória.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Inicializa o cache.
        
        Args:
            max_size: Número máximo de itens no cache
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, tuple[Any, datetime]] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache.
        
        Args:
            key: Chave do item
            
        Returns:
            Valor armazenado ou None se não encontrado/expirado
        """
        if key not in self.cache:
            return None
            
        value, expiry = self.cache[key]
        if expiry < datetime.now():
            del self.cache[key]
            return None
            
        # Move para o fim (LRU)
        self.cache.move_to_end(key)
        return value
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> None:
        """
        Adiciona valor ao cache.
        
        Args:
            key: Chave do item
            value: Valor a ser armazenado
            ttl: Tempo de vida em segundos (opcional)
        """
        # Remove item mais antigo se necessário
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        expiry = (
            datetime.now() + timedelta(seconds=ttl)
            if ttl
            else datetime.max
        )
        
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """
        Remove valor do cache.
        
        Args:
            key: Chave do item a ser removido
        """
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
    
    def get_size(self) -> int:
        """
        Retorna o número de itens no cache.
        
        Returns:
            Quantidade de itens armazenados
        """
        return len(self.cache)
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do cache.
        
        Returns:
            Dicionário com estatísticas de uso
        """
        expired = sum(
            1 for _, expiry in self.cache.values() 
            if expiry < datetime.now()
        )
        
        return {
            "total_items": len(self.cache),
            "expired_items": expired,
            "active_items": len(self.cache) - expired,
            "max_size": self.max_size,
            "usage_percent": (len(self.cache) / self.max_size) * 100
        } 