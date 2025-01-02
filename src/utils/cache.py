"""Módulo de cache em memória."""
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from collections import OrderedDict
import threading

class InMemoryCache:
    """
    Cache em memória com interface similar ao Redis.
    Implementa LRU (Least Recently Used) para gerenciamento de memória.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Inicializa o cache.
        
        Args:
            max_size: Número máximo de itens no cache
            default_ttl: Tempo padrão de expiração em segundos
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, tuple[Any, datetime]] = OrderedDict()
        self._lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém um valor do cache.
        
        Args:
            key: Chave do item
            
        Returns:
            Valor armazenado ou None se não existir/expirado
        """
        with self._lock:
            if key not in self.cache:
                return None
                
            value, expiry = self.cache[key]
            if expiry < datetime.now():
                del self.cache[key]
                return None
                
            # Move para o final (LRU)
            self.cache.move_to_end(key)
            return value
            
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Armazena um valor no cache.
        
        Args:
            key: Chave do item
            value: Valor a armazenar
            ttl: Tempo de expiração em segundos
        """
        with self._lock:
            # Remove item mais antigo se cache cheio
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
                
            expiry = datetime.now() + timedelta(
                seconds=ttl if ttl is not None else self.default_ttl
            )
            self.cache[key] = (value, expiry)
            
    def delete(self, key: str) -> bool:
        """
        Remove um item do cache.
        
        Args:
            key: Chave do item
            
        Returns:
            bool: True se removido, False se não existia
        """
        with self._lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
            
    def clear(self) -> None:
        """Limpa todo o cache."""
        with self._lock:
            self.cache.clear()
            
    def get_many(self, keys: list[str]) -> Dict[str, Any]:
        """
        Obtém múltiplos valores do cache.
        
        Args:
            keys: Lista de chaves
            
        Returns:
            Dict com valores encontrados
        """
        result = {}
        with self._lock:
            for key in keys:
                value = self.get(key)
                if value is not None:
                    result[key] = value
        return result 