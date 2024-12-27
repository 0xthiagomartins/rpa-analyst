import streamlit as st
from typing import Optional
import json

def render_diagram_editor(mermaid_code: str, on_save: Optional[callable] = None):
    """Renderiza o editor visual de diagrama Mermaid."""
    if 'diagram_editor' not in st.session_state:
        st.session_state.diagram_editor = {
            'code': mermaid_code,
            'show_editor': False,
            'current_node': None,
            'nodes': [],
            'connections': []
        }
    
    # Parse o código Mermaid atual
    try:
        # Extrai nós e conexões do código atual
        lines = mermaid_code.split('\n')
        nodes = []
        connections = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('flowchart TD'):
                continue
            elif '-->' in line:  # Conexão
                parts = line.split('-->')
                from_node = parts[0].strip()
                to_part = parts[1].strip()
                
                # Extrai o label se existir
                if '|' in to_part:
                    label_parts = to_part.split('|')
                    to_node = label_parts[2].strip()
                    label = label_parts[1].strip()
                else:
                    to_node = to_part
                    label = ''
                
                # Remove possíveis colchetes do to_node
                if '[' in to_node:
                    to_node = to_node.split('[')[0].strip()
                
                connections.append({
                    'from': from_node,
                    'to': to_node,
                    'label': label
                })
            elif line and '[' in line:  # Nó
                parts = line.split('[', 1)
                node_id = parts[0].strip()
                node_label = parts[1].rsplit(']', 1)[0]
                
                # Determina o tipo de forma
                shape = 'box'
                if '((' in line and '))' in line:
                    shape = 'circle'
                elif '{' in line and '}' in line:
                    shape = 'diamond'
                elif '{{' in line and '}}' in line:
                    shape = 'hexagon'
                
                nodes.append({
                    'id': node_id,
                    'label': node_label,
                    'shape': shape
                })
        
        st.session_state.diagram_editor['nodes'] = nodes
        st.session_state.diagram_editor['connections'] = connections
        
    except Exception as e:
        st.error(f"Erro ao processar diagrama: {str(e)}")
        st.session_state.diagram_editor['nodes'] = []
        st.session_state.diagram_editor['connections'] = []
    
    # Interface do Editor
    with st.expander("✏️ Editor de Diagrama", expanded=st.session_state.diagram_editor['show_editor']):
        # Tabs para diferentes aspectos do editor
        tab_nodes, tab_connections, tab_style = st.tabs(["Nós", "Conexões", "Estilo"])
        
        with tab_nodes:
            st.write("### Nós do Diagrama")
            
            # Lista de nós existentes
            st.write("**Nós Existentes:**")
            for idx, node in enumerate(st.session_state.diagram_editor['nodes']):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    new_id = st.text_input("ID", node['id'], key=f"node_id_{idx}")
                with col2:
                    new_label = st.text_input("Label", node['label'], key=f"node_label_{idx}")
                with col3:
                    shape = st.selectbox("Forma", 
                                       ["box", "circle", "diamond", "hexagon"],
                                       index=["box", "circle", "diamond", "hexagon"].index(node.get('shape', 'box')),
                                       key=f"node_shape_{idx}")
                with col4:
                    if st.button("🗑️", key=f"del_node_{idx}"):
                        st.session_state.diagram_editor['nodes'].pop(idx)
                        st.rerun()
                
                # Atualiza o nó
                node.update({'id': new_id, 'label': new_label, 'shape': shape})
            
            # Adicionar novo nó
            st.write("**Adicionar Novo Nó:**")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_node_id = st.text_input("ID", key="new_node_id")
            with col2:
                new_node_label = st.text_input("Label", key="new_node_label")
            with col3:
                new_node_shape = st.selectbox("Forma", ["box", "circle", "diamond", "hexagon"])
            
            if st.button("➕ Adicionar Nó"):
                if new_node_id and new_node_label:
                    st.session_state.diagram_editor['nodes'].append({
                        'id': new_node_id,
                        'label': new_node_label,
                        'shape': new_node_shape
                    })
                    st.rerun()
            
            # Organização por tipo
            st.write("### Organização dos Nós")
            node_organization = st.radio(
                "Organizar por:",
                ["Ordem de Criação", "Tipo", "Alfabético"]
            )
            
            nodes = st.session_state.diagram_editor['nodes']
            if node_organization == "Tipo":
                nodes = sorted(nodes, key=lambda x: x['shape'])
            elif node_organization == "Alfabético":
                nodes = sorted(nodes, key=lambda x: x['label'])
        
        with tab_connections:
            st.write("### Conexões")
            
            # Lista de conexões existentes
            st.write("**Conexões Existentes:**")
            for idx, conn in enumerate(st.session_state.diagram_editor['connections']):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    node_ids = [n['id'] for n in st.session_state.diagram_editor['nodes']]
                    try:
                        from_index = node_ids.index(conn['from'])
                    except ValueError:
                        from_index = 0
                        # Adiciona o nó ausente à lista
                        st.session_state.diagram_editor['nodes'].append({
                            'id': conn['from'],
                            'label': conn['from'],
                            'shape': 'box'
                        })
                        
                    from_node = st.selectbox("De", 
                                           node_ids, 
                                           index=from_index,
                                           key=f"conn_from_{idx}")
                with col2:
                    try:
                        to_index = node_ids.index(conn['to'])
                    except ValueError:
                        to_index = 0
                        # Adiciona o nó ausente à lista
                        st.session_state.diagram_editor['nodes'].append({
                            'id': conn['to'],
                            'label': conn['to'],
                            'shape': 'box'
                        })
                        
                    to_node = st.selectbox("Para", 
                                         node_ids,
                                         index=to_index,
                                         key=f"conn_to_{idx}")
                with col3:
                    label = st.text_input("Label", conn.get('label', ''), key=f"conn_label_{idx}")
                with col4:
                    if st.button("🗑️", key=f"del_conn_{idx}"):
                        st.session_state.diagram_editor['connections'].pop(idx)
                        st.rerun()
                
                # Atualiza a conexão
                conn.update({'from': from_node, 'to': to_node, 'label': label})
            
            # Adicionar nova conexão
            st.write("**Adicionar Nova Conexão:**")
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                new_conn_from = st.selectbox("De", [n['id'] for n in st.session_state.diagram_editor['nodes']], key="new_conn_from")
            with col2:
                new_conn_to = st.selectbox("Para", [n['id'] for n in st.session_state.diagram_editor['nodes']], key="new_conn_to")
            with col3:
                new_conn_label = st.text_input("Label", key="new_conn_label")
            
            if st.button("➕ Adicionar Conexão"):
                st.session_state.diagram_editor['connections'].append({
                    'from': new_conn_from,
                    'to': new_conn_to,
                    'label': new_conn_label
                })
                st.rerun()
        
        with tab_style:
            st.write("### Estilo do Diagrama")
            
            # Direção do diagrama
            direction = st.selectbox(
                "Direção do Fluxo",
                ["TD (Top-Down)", "LR (Left-Right)", "RL (Right-Left)", "BT (Bottom-Top)"],
                index=0
            )
            
            # Cores para diferentes tipos de nós
            st.write("**Cores dos Nós**")
            col1, col2 = st.columns(2)
            with col1:
                start_end_color = st.color_picker("Início/Fim", "#f9f9f9")
                action_color = st.color_picker("Ações", "#bbdefb")
            with col2:
                decision_color = st.color_picker("Decisões", "#fff59d")
                system_color = st.color_picker("Sistemas", "#c8e6c9")
            
            # Espessura das linhas
            line_thickness = st.slider("Espessura das Linhas", 1, 5, 2)
            
            # Curvas das conexões
            curve_style = st.selectbox(
                "Estilo das Conexões",
                ["Linha Reta", "Curva Suave", "Ângulo Reto"]
            )
            
            # Aplica os estilos ao gerar o código
            styles = []
            for node in st.session_state.diagram_editor['nodes']:
                if node['shape'] == 'circle':
                    styles.append(f"style {node['id']} fill:{start_end_color},stroke:#333")
                elif node['shape'] == 'diamond':
                    styles.append(f"style {node['id']} fill:{decision_color},stroke:#333")
                elif node['shape'] == 'hexagon':
                    styles.append(f"style {node['id']} fill:{system_color},stroke:#333")
                else:
                    styles.append(f"style {node['id']} fill:{action_color},stroke:#333")
            
            # Gera o novo código Mermaid
            new_code = [f"flowchart {direction.split()[0]}"]
            
            # Adiciona nós
            for node in st.session_state.diagram_editor['nodes']:
                shape_start, shape_end = {
                    'box': ['[', ']'],
                    'circle': ['((', '))'],
                    'diamond': ['{', '}'],
                    'hexagon': ['{{', '}}']
                }.get(node['shape'], ['[', ']'])
                
                new_code.append(f"{node['id']}{shape_start}{node['label']}{shape_end}")
            
            # Adiciona conexões
            for conn in st.session_state.diagram_editor['connections']:
                if conn['label']:
                    new_code.append(f"{conn['from']} --> |{conn['label']}| {conn['to']}")
                else:
                    new_code.append(f"{conn['from']} --> {conn['to']}")
            
            # Atualiza o código
            st.session_state.diagram_editor['code'] = '\n'.join(new_code)
            
            # Preview do diagrama
            st.write("### Preview")
            st.markdown(f"""
            ```mermaid
            {st.session_state.diagram_editor['code']}
            ```
            """)
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar Alterações", use_container_width=True):
                if on_save:
                    on_save(st.session_state.diagram_editor['code'])
                st.success("Diagrama atualizado com sucesso!")
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.diagram_editor['show_editor'] = False
                st.rerun()

    return st.session_state.diagram_editor['code']

def validate_node(node_id: str, node_label: str) -> tuple[bool, str]:
    """Valida um nó antes de adicionar/atualizar."""
    if not node_id:
        return False, "ID do nó não pode estar vazio"
    if not node_label:
        return False, "Label do nó não pode estar vazio"
    if ' ' in node_id:
        return False, "ID do nó não pode conter espaços"
    if any(c in node_id for c in '[]{}()'):
        return False, "ID do nó não pode conter caracteres especiais"
    return True, ""

# Adicionar templates
st.write("### Templates")
template = st.selectbox(
    "Carregar Template",
    ["Personalizado", "Processo Linear", "Processo com Decisões", "Integração de Sistemas"]
)

if template != "Personalizado" and st.button("Carregar Template"):
    if template == "Processo Linear":
        # Carrega template de processo linear
        nodes = [
            {"id": "start", "label": "Início", "shape": "circle"},
            {"id": "step1", "label": "Etapa 1", "shape": "box"},
            {"id": "step2", "label": "Etapa 2", "shape": "box"},
            {"id": "end", "label": "Fim", "shape": "circle"}
        ]
        connections = [
            {"from": "start", "to": "step1", "label": ""},
            {"from": "step1", "to": "step2", "label": ""},
            {"from": "step2", "to": "end", "label": ""}
        ]
    # ... outros templates