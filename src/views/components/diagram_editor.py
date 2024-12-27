"""
Editor de Diagramas de Processo

Este módulo implementa um editor visual de diagramas de processo usando Streamlit.
Principais funcionalidades:
- Criação e edição de nós
- Conexões entre nós
- Sistema de undo/redo
- Validação em tempo real
- Feedback visual de ações
- Cache de estados

Uso básico:
```python
editor = DiagramEditor()
editor.render_diagram_editor()
```

Classes:
- DiagramState: Representa um estado do diagrama
- DiagramEditor: Editor visual de diagramas
"""

from typing import List, Dict, Optional
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from src.utils.diagram_validator import DiagramValidator
from src.services.mermaid_service import MermaidService
import copy
import json

class DiagramState:
    """Classe para representar um estado do diagrama."""
    def __init__(self, nodes: List[Dict], edges: List[Dict], selected_node: Optional[str] = None):
        self.nodes = copy.deepcopy(nodes)
        self.edges = copy.deepcopy(edges)
        self.selected_node = selected_node
    
    def to_dict(self) -> Dict:
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'selected_node': self.selected_node
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DiagramState':
        return cls(
            nodes=data['nodes'],
            edges=data['edges'],
            selected_node=data['selected_node']
        )

class DiagramEditor:
    """Editor visual de diagramas de processo."""
    
    NODE_TYPES = {
        'start': {'label': '🟢 Início', 'color': '#f9f9f9'},
        'action': {'label': '🔷 Ação', 'color': '#bbdefb'},
        'decision': {'label': '💠 Decisão', 'color': '#fff59d'},
        'system': {'label': '🖥️ Sistema', 'color': '#c8e6c9'},
        'end': {'label': '🔴 Fim', 'color': '#f9f9f9'}
    }
    
    MAX_HISTORY_SIZE = 30  # Limite máximo de estados no histórico
    
    def __init__(self):
        # Inicializa o estado do diagrama
        if 'diagram_state' not in st.session_state:
            st.session_state.diagram_state = {
                'nodes': self._convert_steps_to_nodes(),
                'edges': [],
                'selected_node': None,
                'history': [],
                'history_index': -1,
                'editing_edge': False
            }
            # Salva estado inicial
            self._save_state()
            
        self.validator = DiagramValidator()
        self.mermaid_service = MermaidService()
    
    def _save_state(self):
        """Salva o estado atual no histórico."""
        # Faz uma cópia profunda do estado atual
        current_state = DiagramState(
            nodes=copy.deepcopy(st.session_state.diagram_state['nodes']),
            edges=copy.deepcopy(st.session_state.diagram_state['edges']),
            selected_node=st.session_state.diagram_state['selected_node']
        )
        
        # Remove estados futuros se estiver no meio do histórico
        history = st.session_state.diagram_state['history']
        index = st.session_state.diagram_state['history_index']
        
        if index < len(history) - 1:
            history = history[:index + 1]
        
        # Limita o tamanho do histórico removendo os estados mais antigos
        if len(history) >= self.MAX_HISTORY_SIZE:
            remove_count = self.MAX_HISTORY_SIZE // 4
            history = history[remove_count:]
            index = len(history) - 1
        
        # Adiciona novo estado
        state_dict = current_state.to_dict()
        
        # Garante que os IDs são sequenciais no novo estado
        nodes = state_dict['nodes']
        for i, node in enumerate(nodes):
            old_id = node['id']
            new_id = f'node_{i}'
            node['id'] = new_id
            
            # Atualiza referências nas arestas
            for edge in state_dict['edges']:
                if edge['source'] == old_id:
                    edge['source'] = new_id
                if edge['target'] == old_id:
                    edge['target'] = new_id
        
        # Adiciona ao histórico
        history.append(copy.deepcopy(state_dict))
        st.session_state.diagram_state['history'] = history
        st.session_state.diagram_state['history_index'] = len(history) - 1
        
        # Atualiza o estado atual
        st.session_state.diagram_state['nodes'] = copy.deepcopy(nodes)
        st.session_state.diagram_state['edges'] = copy.deepcopy(state_dict['edges'])
    
    def undo(self):
        """Desfaz última ação."""
        if st.session_state.diagram_state['history_index'] > 0:
            st.session_state.diagram_state['history_index'] -= 1
            self._restore_state(st.session_state.diagram_state['history_index'])
            st.rerun()
    
    def redo(self):
        """Refaz última ação desfeita."""
        history = st.session_state.diagram_state['history']
        index = st.session_state.diagram_state['history_index']
        
        if index < len(history) - 1:
            st.session_state.diagram_state['history_index'] += 1
            self._restore_state(st.session_state.diagram_state['history_index'])
            st.rerun()
    
    def _restore_state(self, index: int):
        """Restaura um estado específico do histórico."""
        state = DiagramState.from_dict(
            st.session_state.diagram_state['history'][index]
        )
        
        # Faz uma cópia profunda dos dados para evitar referências
        st.session_state.diagram_state.update({
            'nodes': copy.deepcopy(state.nodes),
            'edges': copy.deepcopy(state.edges),
            'selected_node': state.selected_node
        })
    
    def _convert_steps_to_nodes(self) -> List[Dict]:
        """Converte as etapas do processo em nós do diagrama."""
        if 'process_steps' not in st.session_state:
            return []
            
        return [
            {
                'id': step['id'],
                'name': step['name'],
                'type': step.get('type', 'action'),
                'description': step.get('description', ''),
                'dependencies': step.get('dependencies', [])
            }
            for step in st.session_state.process_steps
        ]
    
    def _sync_with_process_steps(self):
        """Sincroniza o diagrama com as etapas do processo."""
        # Atualiza os nós com base nas etapas
        current_nodes = {node['id']: node for node in st.session_state.diagram_state['nodes']}
        process_steps = {step['id']: step for step in st.session_state.process_steps}
        
        # Adiciona novos nós
        for step_id, step in process_steps.items():
            if step_id not in current_nodes:
                new_node = {
                    'id': step_id,
                    'name': step['name'],
                    'type': step.get('type', 'action'),
                    'description': step.get('description', ''),
                    'dependencies': step.get('dependencies', [])
                }
                st.session_state.diagram_state['nodes'].append(new_node)
        
        # Remove nós que não existem mais nas etapas
        st.session_state.diagram_state['nodes'] = [
            node for node in st.session_state.diagram_state['nodes']
            if node['id'] in process_steps
        ]
        
        # Atualiza as conexões com base nas sugestões da IA
        if 'ai_suggestions' in st.session_state and 'connections' in st.session_state.ai_suggestions:
            suggested_connections = st.session_state.ai_suggestions['connections']
            
            # Converte sugestões em arestas
            edges = []
            for conn in suggested_connections:
                if conn['source'] in process_steps and conn['target'] in process_steps:
                    edge = {
                        'source': conn['source'],
                        'target': conn['target'],
                        'label': conn.get('label', ''),
                        'type': conn.get('type', 'sequential')
                    }
                    edges.append(edge)
            
            # Atualiza as arestas no estado
            st.session_state.diagram_state['edges'] = edges
            
            # Salva o estado
            self._save_state()
    
    def render_canvas(self):
        """Renderiza a área principal do diagrama."""
        nodes = []
        edges = []
        
        # Converte nós para formato do agraph
        for node in st.session_state.diagram_state['nodes']:
            nodes.append(Node(
                id=node['id'],
                label=node['name'],
                size=25,
                color=self.NODE_TYPES[node['type']]['color'],
                shape='dot' if node['type'] in ['start', 'end'] else 'box'
            ))
        
        # Converte arestas
        for edge in st.session_state.diagram_state['edges']:
            edges.append(Edge(
                source=edge['source'],
                target=edge['target'],
                label=edge.get('label', ''),
                type="CURVE_SMOOTH"
            ))
        
        # Configuração do diagrama
        config = Config(
            width=800,
            height=500,
            directed=True,
            physics=True,
            hierarchical=True,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )
        
        # Renderiza o diagrama interativo
        selected = agraph(
            nodes=nodes, 
            edges=edges, 
            config=config
        )
        
        # Atualiza o nó selecionado se houver mudança
        if selected and selected != st.session_state.diagram_state['selected_node']:
            st.session_state.diagram_state['selected_node'] = selected
            st.rerun()
    
    def render_toolbar(self):
        """Renderiza a barra de ferramentas."""
        st.write("### 🛠️ Ferramentas")
        
        # Status do histórico
        history_index = st.session_state.diagram_state['history_index']
        history_len = len(st.session_state.diagram_state['history'])
        
        # Primeira linha - Operações básicas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            can_undo = history_index > 0
            if st.button(
                "⬅️ Desfazer", 
                key="btn_undo", 
                use_container_width=True,
                disabled=not can_undo,
                help="Desfaz a última ação" if can_undo else "Não há ações para desfazer"
            ):
                self.undo()
                st.toast("Ação desfeita", icon="↩️")
        
        with col2:
            can_redo = history_index < history_len - 1
            if st.button(
                "➡️ Refazer", 
                key="btn_redo", 
                use_container_width=True,
                disabled=not can_redo,
                help="Refaz a última ação desfeita" if can_redo else "Não há ações para refazer"
            ):
                self.redo()
                st.toast("Ação refeita", icon="↪️")
        
        with col3:
            if st.button(
                "➕ Novo", 
                key="btn_new_node", 
                use_container_width=True,
                help="Adiciona um novo nó ao diagrama"
            ):
                self._add_new_node()
                self._save_state()
                st.toast("Novo nó adicionado", icon="➕")
        
        with col4:
            if st.button(
                "🔗 Conectar", 
                key="btn_connect", 
                use_container_width=True,
                help="Cria uma conexão entre dois nós"
            ):
                if len(st.session_state.diagram_state['nodes']) < 2:
                    st.warning("Adicione pelo menos 2 nós para criar uma conexão")
                else:
                    st.session_state.diagram_state['editing_edge'] = True
                    st.toast("Modo de conexão ativado", icon="🔗")
        
        with col5:
            can_delete = st.session_state.diagram_state['selected_node'] is not None
            if st.button(
                "🗑️ Excluir", 
                key="btn_delete", 
                use_container_width=True,
                disabled=not can_delete,
                help="Exclui o nó selecionado" if can_delete else "Selecione um nó para excluir"
            ):
                node_name = self._get_selected_node().get('name', 'Nó')
                self._delete_selected()
                self._save_state()
                st.toast(f"{node_name} excluído", icon="🗑️")
        
        # Barra de progresso do histórico
        st.progress(
            (history_index + 1) / max(history_len, 1),
            text=f"Histórico: {history_index + 1}/{history_len}"
        )
    
    def render_properties_panel(self):
        """Renderiza o painel de propriedades."""
        if st.session_state.diagram_state['selected_node']:
            st.write("### ⚙️ Propriedades")
            node = self._get_selected_node()
            
            if node:
                # Nome do nó
                new_name = st.text_input(
                    "Nome:",
                    value=node.get('name', ''),
                    key="input_node_name"
                )
                
                # Tipo do nó
                new_type = st.selectbox(
                    "Tipo:",
                    options=list(self.NODE_TYPES.keys()),
                    format_func=lambda x: self.NODE_TYPES[x]['label'],
                    index=list(self.NODE_TYPES.keys()).index(node.get('type', 'action')),
                    key="select_node_type"
                )
                
                # Descrição (opcional)
                new_description = st.text_area(
                    "Descrição:",
                    value=node.get('description', ''),
                    key="input_node_description"
                )
                
                # Atualiza o nó se houver mudanças
                if (new_name != node.get('name') or 
                    new_type != node.get('type') or 
                    new_description != node.get('description')):
                    self._update_node(node['id'], {
                        'name': new_name,
                        'type': new_type,
                        'description': new_description
                    })
        
        # Modo de edição de conexão
        elif st.session_state.diagram_state['editing_edge']:
            st.write("### 🔗 Nova Conexão")
            self._render_edge_editor()
    
    def _render_edge_editor(self):
        """Renderiza o editor de conexões."""
        nodes = st.session_state.diagram_state['nodes']
        
        if len(nodes) < 2:
            st.warning("Adicione pelo menos 2 nós para criar uma conexão")
            return
        
        with st.form("edge_editor"):
            st.write("### 🔗 Nova Conexão")
            
            # Seleção de nós
            source = st.selectbox(
                "De:",
                options=[n['id'] for n in nodes],
                format_func=lambda x: next(n['name'] for n in nodes if n['id'] == x),
                key="select_edge_source"
            )
            
            target = st.selectbox(
                "Para:",
                options=[n['id'] for n in nodes if n['id'] != source],
                format_func=lambda x: next(n['name'] for n in nodes if n['id'] == x),
                key="select_edge_target"
            )
            
            # Label opcional
            label = st.text_input("Rótulo (opcional):", key="input_edge_label")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Confirmar", use_container_width=True):
                    self._add_edge(source, target, label)
                    self._save_state()
                    st.session_state.diagram_state['editing_edge'] = False
                    st.toast("Conexão criada", icon="🔗")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("Cancelar", use_container_width=True):
                    st.session_state.diagram_state['editing_edge'] = False
                    st.rerun()
    
    def _add_edge(self, source: str, target: str, label: str = ""):
        """Adiciona uma nova conexão ao diagrama."""
        if source and target and source != target:
            edge = {
                'source': source,
                'target': target,
                'label': label
            }
            st.session_state.diagram_state['edges'].append(edge)
    
    def _update_node(self, node_id: str, properties: Dict):
        """Atualiza as propriedades de um nó."""
        nodes = st.session_state.diagram_state['nodes']
        for i, node in enumerate(nodes):
            if node['id'] == node_id:
                nodes[i].update(properties)
                break
    
    def _add_new_node(self):
        """Adiciona um novo nó ao diagrama."""
        # Encontra o maior ID atual
        current_nodes = st.session_state.diagram_state['nodes']
        max_id = -1
        for node in current_nodes:
            if node['id'].startswith('node_'):
                try:
                    num = int(node['id'].split('_')[1])
                    max_id = max(max_id, num)
                except ValueError:
                    continue
        
        new_id = f"node_{max_id + 1}"
        new_node = {
            'id': new_id,
            'name': f"Nova Etapa {max_id + 2}",
            'type': 'action'
        }
        st.session_state.diagram_state['nodes'].append(new_node)
    
    def _delete_selected(self):
        """Remove o nó ou conexão selecionada."""
        if st.session_state.diagram_state['selected_node']:
            # Remove o nó
            nodes = st.session_state.diagram_state['nodes']
            nodes = [n for n in nodes if n['id'] != st.session_state.diagram_state['selected_node']]
            st.session_state.diagram_state['nodes'] = nodes
            
            # Remove as conexões relacionadas
            edges = st.session_state.diagram_state['edges']
            edges = [e for e in edges if e['source'] != st.session_state.diagram_state['selected_node'] 
                    and e['target'] != st.session_state.diagram_state['selected_node']]
            st.session_state.diagram_state['edges'] = edges
            
            st.session_state.diagram_state['selected_node'] = None
    
    def _get_selected_node(self) -> Dict:
        """Retorna o nó selecionado."""
        if st.session_state.diagram_state['selected_node']:
            for node in st.session_state.diagram_state['nodes']:
                if node['id'] == st.session_state.diagram_state['selected_node']:
                    return node
        return {}
    
    def _validate_diagram(self):
        """Valida o diagrama atual."""
        is_valid, errors = self.validator.validate_diagram(
            st.session_state.diagram_state['nodes'],
            st.session_state.diagram_state['edges']
        )
        
        if is_valid:
            st.success("✅ Diagrama válido!")
        else:
            st.error("❌ Problemas encontrados no diagrama:")
            for error in errors:
                st.warning(f"• {error}")

def render_diagram_editor():
    """Função principal para renderizar o editor de diagrama."""
    editor = DiagramEditor()
    
    # Layout principal
    st.write("## 📊 Editor de Diagrama")
    
    # Divide a tela em duas colunas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Container para o diagrama
        with st.container():
            # Área principal do diagrama
            editor.render_canvas()
    
    with col2:
        # Barra de ferramentas e propriedades
        editor.render_toolbar()
        st.divider()
        editor.render_properties_panel()