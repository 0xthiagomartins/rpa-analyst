from typing import List, Dict
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from src.utils.diagram_validator import DiagramValidator
from src.services.mermaid_service import MermaidService

class DiagramEditor:
    """Editor visual de diagramas de processo."""
    
    NODE_TYPES = {
        'start': {'label': '🟢 Início', 'color': '#f9f9f9'},
        'action': {'label': '🔷 Ação', 'color': '#bbdefb'},
        'decision': {'label': '💠 Decisão', 'color': '#fff59d'},
        'system': {'label': '🖥️ Sistema', 'color': '#c8e6c9'},
        'end': {'label': '🔴 Fim', 'color': '#f9f9f9'}
    }
    
    def __init__(self):
        if 'diagram_state' not in st.session_state:
            st.session_state.diagram_state = {
                'selected_node': None,
                'nodes': self._convert_steps_to_nodes(),
                'edges': [],
                'canvas_scale': 1.0,
                'canvas_offset': {'x': 0, 'y': 0},
                'editing_edge': False
            }
        self.validator = DiagramValidator()
        self.mermaid_service = MermaidService()
    
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
        
        # Atualiza as conexões com base nas dependências
        edges = []
        for node in st.session_state.diagram_state['nodes']:
            for dep in node.get('dependencies', []):
                edges.append({
                    'source': dep,
                    'target': node['id'],
                    'label': 'depende de'
                })
        st.session_state.diagram_state['edges'] = edges
    
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
        
        # Primeira linha - Operações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Novo Nó", key="btn_new_node", use_container_width=True):
                self._add_new_node()
        
        with col2:
            if st.button("🔗 Conectar", key="btn_connect", use_container_width=True):
                st.session_state.diagram_state['editing_edge'] = True
        
        with col3:
            if st.button("🗑️ Excluir", key="btn_delete", use_container_width=True):
                self._delete_selected()
        
        # Segunda linha - Ferramentas adicionais
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Sincronizar", key="btn_sync", use_container_width=True):
                self._sync_with_process_steps()
        
        with col2:
            if st.button("✅ Validar", key="btn_validate", use_container_width=True):
                self._validate_diagram()
    
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
            if st.button("Confirmar", key="btn_confirm_edge", use_container_width=True):
                self._add_edge(source, target, label)
                st.session_state.diagram_state['editing_edge'] = False
                st.rerun()
        
        with col2:
            if st.button("Cancelar", key="btn_cancel_edge", use_container_width=True):
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
        new_id = f"node_{len(st.session_state.diagram_state['nodes'])}"
        new_node = {
            'id': new_id,
            'name': f"Nova Etapa {len(st.session_state.diagram_state['nodes']) + 1}",
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