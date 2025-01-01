class FlowEditor:
    """Editor visual de fluxo do processo."""
    
    def render(self):
        """Renderiza o editor de fluxo."""
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Lista de passos
            self._render_steps_list()
            
        with col2:
            # Preview do diagrama
            self._render_diagram_preview()
    
    def _render_steps_list(self):
        """Renderiza lista editável de passos."""
        st.write("### Passos do Processo")
        
        for i, step in enumerate(st.session_state.steps_list):
            with st.expander(f"{i+1}. {step['description']}", expanded=False):
                # Edição básica do passo
                new_desc = st.text_input("Descrição", step['description'])
                new_type = st.selectbox(
                    "Tipo",
                    options=['start', 'process', 'decision', 'delay', 'end'],
                    index=['start', 'process', 'decision', 'delay', 'end'].index(step['type'])
                )
                
                # Gerenciamento de conexões
                st.write("#### Conexões")
                for conn in step['connections']:
                    cols = st.columns([3, 2, 1])
                    with cols[0]:
                        # Dropdown com todos os outros passos
                        target_steps = [s for s in st.session_state.steps_list if s['id'] != step['id']]
                        target_index = next(
                            (i for i, s in enumerate(target_steps) if s['id'] == conn['target']), 
                            0
                        )
                        new_target = st.selectbox(
                            "Conectar a",
                            options=[s['description'] for s in target_steps],
                            index=target_index
                        )
                    
                    with cols[1]:
                        new_desc = st.text_input("Descrição", conn['description'])
                    
                    with cols[2]:
                        if st.button("🗑️", key=f"del_conn_{step['id']}_{conn['target']}"):
                            step['connections'].remove(conn)
                            st.rerun()
                
                # Adicionar nova conexão
                if st.button("➕ Adicionar Conexão", key=f"add_conn_{step['id']}"):
                    step['connections'].append({
                        "target": "",
                        "description": "Nova conexão"
                    })
                    st.rerun()
    
    def _render_diagram_preview(self):
        """Renderiza preview do diagrama."""
        st.write("### Preview do Diagrama")
        
        # Gera e mostra diagrama
        flowchart = FlowchartGenerator()
        mermaid_code = flowchart.convert_to_mermaid({
            "steps": st.session_state.steps_list
        })
        
        st.markdown(f"""
        ```mermaid
        {mermaid_code}
        ```
        """) 