import streamlit as st
from streamlit_mermaid import st_mermaid
from src.services.ai_service import AIService
from typing import List

def render_diagram_editor(process_description: str, steps: List[str]):
    """Renderiza o editor de diagrama."""
    st.write("### Diagrama do Processo")
    
    # Botão para gerar diagrama
    if st.button("🤖 Gerar Diagrama com IA"):
        with st.spinner("Gerando diagrama..."):
            try:
                ai_service = AIService()
                diagram = ai_service.generate_diagram(process_description, steps)
                
                # Salva o diagrama no estado da sessão
                st.session_state.current_diagram = diagram.diagram_code
                st.session_state.diagram_explanation = diagram.explanation
                
                st.success("Diagrama gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao gerar diagrama: {str(e)}")
    
    # Editor do diagrama
    if 'current_diagram' in st.session_state:
        st.write("#### Editor do Diagrama")
        
        # Área de edição
        new_diagram = st.text_area(
            "Código Mermaid:",
            value=st.session_state.current_diagram,
            height=300,
            help="Edite o código Mermaid para customizar o fluxograma"
        )
        
        # Preview do diagrama
        if new_diagram:
            st.write("#### Preview")
            try:
                # Garante que o diagrama use a sintaxe correta
                if not any(syntax in new_diagram for syntax in ["flowchart TD", "graph TD"]):
                    new_diagram = new_diagram.replace("graph", "flowchart")
                
                # Renderiza o diagrama
                st_mermaid(new_diagram)
                
                # Botão de salvar
                if st.button("💾 Salvar Alterações"):
                    st.session_state.current_diagram = new_diagram
                    st.success("Diagrama atualizado!")
                
            except Exception as e:
                st.error(f"Erro ao renderizar diagrama: {str(e)}")
        
        # Explicação do diagrama
        if 'diagram_explanation' in st.session_state:
            with st.expander("💡 Explicação do Diagrama", expanded=False):
                st.write(st.session_state.diagram_explanation)