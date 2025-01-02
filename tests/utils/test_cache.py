"""Testes para o módulo de cache."""
import pytest
from datetime import datetime, timedelta
from time import sleep
import threading
from src.utils.cache import InMemoryCache

@pytest.fixture
def cache():
    """Fixture que fornece uma instância limpa do cache."""
    return InMemoryCache(max_size=3, default_ttl=60)

def test_set_and_get(cache):
    """Testa operações básicas de set e get."""
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert cache.get("nonexistent") is None

def test_ttl_expiration(cache):
    """Testa expiração de itens."""
    # Item com TTL curto
    cache.set("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"
    sleep(1.1)  # Espera expirar
    assert cache.get("key1") is None
    
    # Item com TTL padrão
    cache.set("key2", "value2")
    assert cache.get("key2") == "value2"

def test_lru_eviction(cache):
    """Testa política de remoção LRU."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    # Acessa key1, movendo para o final
    cache.get("key1")
    
    # Adiciona novo item, deve remover key2 (menos recente)
    cache.set("key4", "value4")
    
    assert cache.get("key2") is None
    assert cache.get("key1") == "value1"
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"

def test_thread_safety():
    """Testa thread-safety do cache."""
    cache = InMemoryCache(max_size=1000)
    
    def worker():
        for i in range(100):
            cache.set(f"key{i}", f"value{i}")
            cache.get(f"key{i}")
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        
    # Verifica se não houve corrupção
    for i in range(100):
        value = cache.get(f"key{i}")
        if value is not None:
            assert value == f"value{i}"

def test_get_many(cache):
    """Testa obtenção de múltiplos valores."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    result = cache.get_many(["key1", "key2", "nonexistent"])
    assert result == {
        "key1": "value1",
        "key2": "value2"
    }

def test_delete(cache):
    """Testa remoção de itens."""
    cache.set("key1", "value1")
    assert cache.delete("key1") is True
    assert cache.get("key1") is None
    assert cache.delete("nonexistent") is False

def test_clear(cache):
    """Testa limpeza do cache."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None 