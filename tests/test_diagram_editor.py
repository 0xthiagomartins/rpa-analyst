import pytest
from src.views.components.diagram_editor import DiagramEditor, DiagramState
import streamlit as st
from unittest.mock import MagicMock, patch
from typing import Dict, Any

class MockSessionState(dict):
    """Mock para o session_state do Streamlit."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

@pytest.fixture
def mock_session_state():
    """Fixture para simular o session_state do Streamlit."""
    with patch('streamlit.session_state', new=MockSessionState()) as mock_state:
        yield mock_state

@pytest.fixture
def mock_streamlit():
    """Fixture para mockar funções do Streamlit."""
    with patch('streamlit.button', return_value=False) as mock_button, \
         patch('streamlit.write') as mock_write, \
         patch('streamlit.rerun') as mock_rerun:
        yield {
            'button': mock_button,
            'write': mock_write,
            'rerun': mock_rerun
        }

@pytest.fixture
def editor(mock_session_state, mock_streamlit):
    """Fixture para criar uma instância do DiagramEditor."""
    # Inicializa com alguns dados de teste
    mock_session_state.process_steps = []
    return DiagramEditor()

def test_diagram_state_initialization(editor, mock_session_state):
    """Testa a inicialização correta do estado do diagrama."""
    assert hasattr(mock_session_state, 'diagram_state')
    state = mock_session_state.diagram_state
    assert isinstance(state, dict)
    assert 'nodes' in state
    assert 'edges' in state
    assert 'history' in state
    assert 'history_index' in state
    assert state['history_index'] == 0  # Estado inicial

def test_add_node_with_undo(editor, mock_session_state):
    """Testa adição de nó com undo."""
    # Estado inicial
    initial_nodes = len(mock_session_state.diagram_state['nodes'])
    
    # Adiciona um nó
    editor._add_new_node()
    editor._save_state()
    
    # Verifica se o nó foi adicionado
    assert len(mock_session_state.diagram_state['nodes']) == initial_nodes + 1
    
    # Desfaz a ação
    editor.undo()
    
    # Verifica se voltou ao estado inicial
    assert len(mock_session_state.diagram_state['nodes']) == initial_nodes

def test_redo_after_undo(editor, mock_session_state):
    """Testa redo após undo."""
    # Adiciona um nó
    editor._add_new_node()
    editor._save_state()
    
    # Desfaz
    editor.undo()
    
    # Refaz
    editor.redo()
    
    # Verifica se o nó foi restaurado
    assert len(mock_session_state.diagram_state['nodes']) == 1

def test_multiple_operations(editor, mock_session_state):
    """Testa múltiplas operações de undo/redo."""
    # Adiciona três nós
    for _ in range(3):
        editor._add_new_node()
        editor._save_state()
    
    # Desfaz duas vezes
    editor.undo()
    editor.undo()
    
    # Verifica se voltou dois estados
    assert len(mock_session_state.diagram_state['nodes']) == 1
    
    # Refaz uma vez
    editor.redo()
    
    # Verifica se avançou um estado
    assert len(mock_session_state.diagram_state['nodes']) == 2

def test_edge_operations(editor, mock_session_state):
    """Testa operações com arestas."""
    # Adiciona dois nós
    editor._add_new_node()
    editor._add_new_node()
    editor._save_state()
    
    # Adiciona uma aresta
    editor._add_edge('node_0', 'node_1', 'test')
    editor._save_state()
    
    # Verifica se a aresta foi adicionada
    assert len(mock_session_state.diagram_state['edges']) == 1
    
    # Desfaz
    editor.undo()
    
    # Verifica se a aresta foi removida
    assert len(mock_session_state.diagram_state['edges']) == 0

def test_state_limit(editor, mock_session_state):
    """Testa limite de estados no histórico."""
    # Adiciona mais nós que o limite
    for i in range(40):  # MAX_HISTORY_SIZE é 30
        editor._add_new_node()
        editor._save_state()
    
    history = mock_session_state.diagram_state['history']
    
    # Verifica se o histórico está limitado
    assert len(history) <= editor.MAX_HISTORY_SIZE
    
    # Verifica se os estados mais antigos foram removidos
    total_nodes = len(history[-1]['nodes'])
    assert total_nodes == 40, "Deve manter todos os nós mesmo com histórico limitado"
    
    # Verifica se os IDs são sequenciais no último estado
    nodes = history[-1]['nodes']
    node_ids = [int(node['id'].split('_')[1]) for node in nodes]
    assert node_ids == list(range(total_nodes)), "IDs devem ser sequenciais"
    
    # Verifica se as arestas mantêm referências válidas
    for state in history:
        for edge in state['edges']:
            source_id = int(edge['source'].split('_')[1])
            target_id = int(edge['target'].split('_')[1])
            assert 0 <= source_id < total_nodes
            assert 0 <= target_id < total_nodes

def test_invalid_operations(editor, mock_session_state):
    """Testa operações inválidas."""
    # Tenta desfazer sem histórico
    editor.undo()
    assert mock_session_state.diagram_state['history_index'] == 0
    
    # Tenta refazer sem ações desfeitas
    editor.redo()
    assert mock_session_state.diagram_state['history_index'] == 0

def test_node_update(editor, mock_session_state):
    """Testa atualização de propriedades do nó."""
    # Adiciona um nó
    editor._add_new_node()
    editor._save_state()
    
    # Atualiza propriedades
    editor._update_node('node_0', {'name': 'Updated Node'})
    editor._save_state()
    
    # Verifica se a atualização foi salva
    node = next(n for n in mock_session_state.diagram_state['nodes'] if n['id'] == 'node_0')
    assert node['name'] == 'Updated Node'
    
    # Desfaz
    editor.undo()
    
    # Verifica se voltou ao nome original
    node = next(n for n in mock_session_state.diagram_state['nodes'] if n['id'] == 'node_0')
    assert node['name'] != 'Updated Node' 