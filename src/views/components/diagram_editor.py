import streamlit as st
from streamlit_mermaid import st_mermaid
from src.services.ai_service import AIService
from typing import List, Optional

def render_diagram_editor(process_description: str, steps: List[str]):
    """Renderiza o editor de diagrama."""
    st.write("### Diagrama do Processo")
    
    # Inicializa o estado do diagrama se necessário
    if 'diagram_history' not in st.session_state:
        st.session_state.diagram_history = []
    
    # Botão para gerar diagrama
    if not st.session_state.diagram_history and st.button("🤖 Gerar Diagrama com IA"):
        with st.spinner("Gerando diagrama..."):
            try:
                ai_service = AIService()
                diagram = ai_service.generate_diagram(process_description, steps)
                
                # Salva o diagrama no histórico
                st.session_state.diagram_history.append({
                    'diagram_code': diagram.diagram_code,
                    'explanation': diagram.explanation,
                    'feedback': None
                })
                
                st.success("Diagrama gerado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao gerar diagrama: {str(e)}")
    
    # Mostra o diagrama atual e opções de edição
    if st.session_state.diagram_history:
        current_diagram = st.session_state.diagram_history[-1]
        
        # Preview do diagrama atual
        st.write("#### Preview do Diagrama")
        try:
            st_mermaid(current_diagram['diagram_code'])
        except Exception as e:
            st.error(f"Erro ao renderizar diagrama: {str(e)}")
        
        # Explicação do diagrama
        with st.expander("💡 Explicação do Diagrama", expanded=False):
            st.write(current_diagram['explanation'])
        
        # Opções de interação
        st.write("#### Opções de Edição")
        
        edit_option = st.radio(
            "Deseja fazer alterações no diagrama?",
            ["Não, manter como está", "Sim, editar manualmente", "Sim, pedir para IA ajustar"],
            index=0
        )
        
        if edit_option == "Sim, editar manualmente":
            # Área de edição manual
            new_code = st.text_area(
                "Código Mermaid:",
                value=current_diagram['diagram_code'],
                height=300,
                help="Edite o código Mermaid para customizar o fluxograma"
            )
            
            if new_code != current_diagram['diagram_code']:
                if st.button("💾 Salvar Alterações"):
                    st.session_state.diagram_history.append({
                        'diagram_code': new_code,
                        'explanation': current_diagram['explanation'],
                        'feedback': "Edição manual do usuário"
                    })
                    st.success("Diagrama atualizado!")
                    st.rerun()
        
        elif edit_option == "Sim, pedir para IA ajustar":
            feedback = st.text_area(
                "Descreva as alterações desejadas:",
                help="Explique o que você gostaria de mudar no diagrama"
            )
            
            if st.button("🔄 Gerar Nova Versão"):
                with st.spinner("Ajustando diagrama..."):
                    try:
                        ai_service = AIService()
                        # Envia o histórico completo para contexto
                        new_diagram = ai_service.refine_diagram(
                            process_description=process_description,
                            steps=steps,
                            current_diagram=current_diagram['diagram_code'],
                            feedback=feedback,
                            diagram_history=st.session_state.diagram_history
                        )
                        
                        # Adiciona nova versão ao histórico
                        st.session_state.diagram_history.append({
                            'diagram_code': new_diagram.diagram_code,
                            'explanation': new_diagram.explanation,
                            'feedback': feedback
                        })
                        
                        st.success("Diagrama atualizado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao ajustar diagrama: {str(e)}")
        
        # Histórico de versões
        if len(st.session_state.diagram_history) > 1:
            with st.expander("📜 Histórico de Versões", expanded=False):
                for i, version in enumerate(st.session_state.diagram_history):
                    st.write(f"Versão {i+1}")
                    if version['feedback']:
                        st.write(f"Feedback: {version['feedback']}")
                    st.code(version['diagram_code'], language="mermaid")
                    st.write("---")