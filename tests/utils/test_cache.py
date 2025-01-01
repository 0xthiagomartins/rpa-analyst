"""Testes para o módulo de cache."""
import pytest
from datetime import datetime, timedelta
from time import sleep
from src.utils.cache import InMemoryCache

@pytest.fixture
def cache():
    """Fixture que fornece uma instância limpa do cache."""
    return InMemoryCache(max_size=3)

def test_set_and_get(cache):
    """Testa operações básicas de set e get."""
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert cache.get("nonexistent") is None

def test_ttl(cache):
    """Testa expiração de itens."""
    cache.set("key1", "value1", ttl=1)  # 1 segundo
    assert cache.get("key1") == "value1"
    sleep(1.1)  # Espera expirar
    assert cache.get("key1") is None

def test_lru_eviction(cache):
    """Testa remoção LRU quando cache está cheio."""
    # Cache tem tamanho 3
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    cache.set("key4", "value4")  # Deve remover key1
    
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"

def test_delete(cache):
    """Testa deleção de itens."""
    cache.set("key1", "value1")
    cache.delete("key1")
    assert cache.get("key1") is None

def test_clear(cache):
    """Testa limpeza do cache."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get_size() == 0

def test_get_stats(cache):
    """Testa estatísticas do cache."""
    cache.set("key1", "value1")
    cache.set("key2", "value2", ttl=1)
    sleep(1.1)  # Espera expirar key2
    
    stats = cache.get_stats()
    assert stats["total_items"] == 2
    assert stats["expired_items"] == 1
    assert stats["active_items"] == 1
    assert stats["max_size"] == 3
    assert stats["usage_percent"] == (2/3) * 100

def test_lru_order(cache):
    """Testa ordenação LRU."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    # Acessa key1, movendo para o fim
    cache.get("key1")
    
    # Adiciona novo item, deve remover key2
    cache.set("key4", "value4")
    
    assert cache.get("key2") is None
    assert cache.get("key1") == "value1"
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4" 