import streamlit as st
from src.services.ai_service import AIService
from src.views.components.diagram_editor import render_diagram_editor
import streamlit_mermaid as stmd


def clean_mermaid_code(code: str) -> str:
    """Remove marcações Markdown do código Mermaid."""
    # Remove ```mermaid e ``` do início e fim
    code = code.strip()
    if code.startswith("```mermaid"):
        code = code[len("```mermaid"):].strip()
    if code.endswith("```"):
        code = code[:-3].strip()
    return code

def render_process_diagram(process_data: dict):
    """Renderiza o diagrama do processo."""
    st.write("### Diagrama do Processo")
    
    # Verifica se já existe um diagrama gerado
    if 'diagram_code' not in st.session_state:
        # Mostra botão de gerar diagrama
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🎨 Gerar Diagrama", 
                        type="primary",
                        use_container_width=True):
                with st.spinner("Gerando diagrama do processo..."):
                    try:
                        # Gera o diagrama
                        ai_service = AIService()
                        mermaid_code = ai_service.generate_process_diagram(process_data)
                        
                        # Limpa o código
                        mermaid_code = clean_mermaid_code(mermaid_code)
                        if not mermaid_code.startswith("flowchart"):
                            mermaid_code = "flowchart TD\n" + mermaid_code
                        
                        st.session_state.diagram_code = mermaid_code
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao gerar diagrama: {str(e)}")
    else:
        # Exibe o diagrama
        st.markdown("""
        <style>
        .mermaid {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Garante que o código está limpo antes de renderizar
        diagram_code = clean_mermaid_code(st.session_state.diagram_code)
        stmd.st_mermaid(diagram_code)
        
        # Botões de ação
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔄 Regenerar", use_container_width=True):
                del st.session_state.diagram_code
                st.rerun()
        with col2:
            if st.button("✏️ Editar", use_container_width=True):
                st.session_state.show_editor = True
        with col3:
            if st.button("📋 Ver Código", use_container_width=True):
                st.code(diagram_code, language="mermaid")
        
        # Mostra editor se necessário
        if st.session_state.get('show_editor', False):
            render_diagram_editor(
                diagram_code,
                on_save=lambda code: st.session_state.update({'diagram_code': code})
            ) 