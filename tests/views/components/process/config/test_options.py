import pytest
from pathlib import Path
import yaml
import os
from src.views.components.process.config.options import get_default_options, load_form_options

class BaseMockPath(os.PathLike):
    """Classe base para simular Path nos testes."""
    def __init__(self, path):
        self._path = str(path)
        
    def __fspath__(self):
        return self._path
        
    @property
    def parent(self):
        return BaseMockPath(os.path.dirname(self._path))
        
    def __truediv__(self, other):
        return BaseMockPath(os.path.join(self._path, str(other)))
        
    def __str__(self):
        return self._path
        
    def exists(self):
        return os.path.exists(self._path)
        
    def is_symlink(self):
        return False
        
    def resolve(self):
        return self
        
    def absolute(self):
        return self
        
    def mkdir(self, parents=False, exist_ok=False):
        if not exist_ok and os.path.exists(self._path):
            raise FileExistsError(f"Directory {self._path} already exists")
        os.makedirs(self._path, exist_ok=True)
        
    def joinpath(self, *args):
        return BaseMockPath(os.path.join(self._path, *map(str, args)))
        
    def open(self, mode='r', encoding=None):
        if 'w' in mode:
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
        return open(self._path, mode=mode, encoding=encoding)
        
    @property
    def name(self):
        return os.path.basename(self._path)

@pytest.fixture
def mock_config_file(tmp_path):
    """Cria um arquivo de configuração temporário para testes."""
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "form_options.yaml"
    config_path.touch()
    return str(config_path)

@pytest.fixture
def mock_invalid_config_file(tmp_path):
    """Cria um diretório temporário para arquivo inválido."""
    return str(tmp_path / "nonexistent.yaml")

def test_get_default_options():
    """Testa se as opções padrão são retornadas corretamente."""
    options = get_default_options()
    
    required_keys = [
        'common_tools',
        'data_types',
        'data_formats',
        'data_sources',
        'business_rules_templates',
        'common_exceptions',
        'automation_goals',
        'kpi_templates'
    ]
    
    for key in required_keys:
        assert key in options
        assert isinstance(options[key], list)
        assert len(options[key]) > 0

def test_load_form_options_with_valid_yaml(mock_config_file, monkeypatch):
    """Testa o carregamento de opções de um arquivo YAML válido."""
    test_config = {
        'common_tools': ['Microsoft Excel', 'Microsoft Outlook', 'SAP'],
        'data_types': ['Dados financeiros', 'Documentos fiscais'],
        'data_formats': ['PDF', 'Excel'],
        'data_sources': ['Email', 'Sistema'],
        'business_rules_templates': ['Validação', 'Aprovação'],
        'common_exceptions': ['Erro 1', 'Erro 2'],
        'automation_goals': ['Meta 1', 'Meta 2'],
        'kpi_templates': ['KPI 1', 'KPI 2']
    }
    
    with open(mock_config_file, 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f)
    
    # Mock mais específico para garantir que pegamos o arquivo correto
    def mock_path_new(cls, *args, **kwargs):
        # Se não houver argumentos, retorna um Path normal
        if not args:
            return object.__new__(cls)
            
        path_str = str(args[0])
        # Se for o arquivo de configuração, retorna nosso mock
        if 'form_options.yaml' in path_str:
            return BaseMockPath(mock_config_file)
            
        # Para outros casos, retorna um Path normal
        return object.__new__(cls)
    
    monkeypatch.setattr(Path, "__new__", staticmethod(mock_path_new))
    
    # Limpa o cache de opções para forçar recarregamento
    if hasattr(load_form_options, '_options_cache'):
        del load_form_options._options_cache
    
    options = load_form_options()
    
    for key, value in test_config.items():
        assert options[key] == value, f"Valores diferentes para {key}"

def test_load_form_options_with_invalid_yaml(mock_invalid_config_file, monkeypatch):
    """Testa o fallback para opções padrão quando o YAML é inválido."""
    def mock_path_new(cls, *args, **kwargs):
        if args and 'form_options.yaml' in str(args[0]):
            return BaseMockPath(mock_invalid_config_file)
        return object.__new__(cls)
    
    monkeypatch.setattr(Path, "__new__", staticmethod(mock_path_new))
    
    options = load_form_options()
    default_options = get_default_options()
    assert options == default_options, "Deveria retornar as opções padrão quando o arquivo é inválido"

def test_load_form_options_with_missing_keys(mock_config_file, monkeypatch):
    """Testa se valores padrão são usados para chaves ausentes."""
    partial_config = {
        'common_tools': ['Microsoft Excel', 'Microsoft Outlook']
    }
    
    with open(mock_config_file, 'w', encoding='utf-8') as f:
        yaml.dump(partial_config, f)
    
    def mock_path_new(cls, *args, **kwargs):
        if args and 'form_options.yaml' in str(args[0]):
            return BaseMockPath(mock_config_file)
        return object.__new__(cls)
    
    monkeypatch.setattr(Path, "__new__", staticmethod(mock_path_new))
    
    options = load_form_options()
    default_options = get_default_options()
    
    assert options['common_tools'] == partial_config['common_tools'], "Valores do arquivo não foram mantidos"
    
    for key in default_options:
        if key != 'common_tools':
            assert options[key] == default_options[key], f"Valor padrão não usado para {key}"

def test_load_form_options_with_empty_file(mock_config_file, monkeypatch):
    """Testa se valores padrão são usados quando o arquivo está vazio."""
    with open(mock_config_file, 'w', encoding='utf-8') as f:
        f.write('')
    
    def mock_path_new(cls, *args, **kwargs):
        if args and 'form_options.yaml' in str(args[0]):
            return BaseMockPath(mock_config_file)
        return object.__new__(cls)
    
    monkeypatch.setattr(Path, "__new__", staticmethod(mock_path_new))
    
    options = load_form_options()
    default_options = get_default_options()
    
    assert options == default_options, "Deveria retornar as opções padrão quando o arquivo está vazio" 