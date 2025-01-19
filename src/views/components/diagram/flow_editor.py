from typing import List, Dict, Optional
import streamlit as st
from .flowchart_generator import FlowchartGenerator
from .flow_validator import FlowValidator
from .layout_manager import LayoutManager

class FlowEditor:
    """Editor visual de fluxo do processo."""
    
    def __init__(self):
        """Inicializa o editor de fluxo."""
        if 'steps_list' not in st.session_state:
            st.session_state.steps_list = []
            
        self.generator = FlowchartGenerator()
        self.validator = FlowValidator()
        self.layout_manager = LayoutManager()

    def get_steps(self) -> List[Dict]:
        """Retorna lista de passos do processo."""
        return st.session_state.steps_list

    def render(self) -> None:
        """Renderiza o editor."""
        st.write("## Editor de Fluxo")
        
        # Botões de ação principais
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("➕ Novo Passo"):
                self._add_new_step()
        with col2:
            if st.button("🔄 Auto-organizar"):
                self.layout_manager.auto_organize(self.get_steps())
        
        # Layout principal
        left_col, right_col = st.columns([2, 3])
        
        with left_col:
            self._render_steps_list()
            self._render_connections_editor()
        
        with right_col:
            self._render_diagram_preview()
            self._render_validation_feedback()

    def _add_new_step(self) -> None:
        """Adiciona novo passo ao fluxo."""
        new_step = {
            "id": f"STEP{len(self.get_steps()) + 1:03d}",
            "description": "",
            "type": "process",
            "connections": [],
            "position": {"x": 0, "y": len(self.get_steps()) * 100}
        }
        st.session_state.steps_list.append(new_step)

    def _render_step_editor(self, step: Dict) -> None:
        """Renderiza editor de um passo."""
        with st.expander(f"{step['id']}: {step['description'][:50]}...", expanded=False):
            # Campos básicos
            step['description'] = st.text_area(
                "Descrição",
                value=step['description'],
                key=f"desc_{step['id']}"
            )
            
            step['type'] = st.selectbox(
                "Tipo",
                options=['start', 'process', 'decision', 'delay', 'end'],
                index=['start', 'process', 'decision', 'delay', 'end'].index(step['type']),
                key=f"type_{step['id']}"
            )
            
            # Posição do elemento
            col1, col2 = st.columns(2)
            with col1:
                step['position']['x'] = st.number_input(
                    "Posição X",
                    value=step['position']['x'],
                    key=f"pos_x_{step['id']}"
                )
            with col2:
                step['position']['y'] = st.number_input(
                    "Posição Y",
                    value=step['position']['y'],
                    key=f"pos_y_{step['id']}"
                )
            
            # Botão de remoção
            if st.button("🗑️ Remover", key=f"del_{step['id']}"):
                st.session_state.steps_list.remove(step)
                st.rerun()

    def _render_connections_editor(self) -> None:
        """Renderiza editor de conexões."""
        st.write("### Conexões")
        
        if not self.get_steps():
            st.info("Adicione passos para criar conexões")
            return
            
        # Seleção do passo
        selected_step = st.selectbox(
            "Selecione o Passo",
            options=self.get_steps(),
            format_func=lambda x: f"{x['id']}: {x['description'][:50]}",
            key="connection_step_select"
        )
        
        if selected_step:
            self._render_step_connections(selected_step)

    def _render_step_connections(self, step: Dict) -> None:
        """Renderiza conexões de um passo."""
        st.write(f"#### Conexões de {step['id']}")
        
        # Lista conexões existentes
        for i, conn in enumerate(step['connections']):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                # Dropdown com passos disponíveis
                available_steps = [s for s in self.get_steps() if s['id'] != step['id']]
                target_index = next(
                    (i for i, s in enumerate(available_steps) if s['id'] == conn['target']),
                    0
                )
                new_target = st.selectbox(
                    "Conectar a",
                    options=available_steps,
                    index=target_index,
                    format_func=lambda x: f"{x['id']}: {x['description'][:30]}",
                    key=f"conn_target_{step['id']}_{i}"
                )
                conn['target'] = new_target['id']
            
            with col2:
                conn['condition'] = st.text_input(
                    "Condição",
                    value=conn.get('condition', ''),
                    key=f"conn_cond_{step['id']}_{i}"
                )
            
            with col3:
                if st.button("🗑️", key=f"del_conn_{step['id']}_{i}"):
                    step['connections'].pop(i)
                    st.rerun()
        
        # Botão para adicionar conexão
        if st.button("➕ Nova Conexão", key=f"add_conn_{step['id']}"):
            step['connections'].append({
                "target": "",
                "condition": ""
            })
            st.rerun()

    def _render_diagram_preview(self) -> None:
        """Renderiza preview do diagrama."""
        st.write("### Diagrama")
        
        try:
            mermaid_code = self.generator.generate_diagram(
                self.get_steps(),
                self.layout_manager.get_layout()
            )
            
            st.markdown(f"""
            ```mermaid
            {mermaid_code}
            ```
            """)
            
        except Exception as e:
            st.error(f"Erro ao gerar diagrama: {str(e)}")

    def _render_validation_feedback(self) -> None:
        """Renderiza feedback de validação."""
        issues = self.validator.validate_flow(self.get_steps())
        
        if issues:
            with st.expander("⚠️ Problemas Encontrados"):
                for issue in issues:
                    st.warning(issue)
        else:
            st.success("✅ Fluxo válido") 