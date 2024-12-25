import streamlit as st
from src.services.ai_service import AIService
from typing import Optional

def render_description_formalizer(
    current_description: str,
    on_update: callable,
    key_prefix: Optional[str] = None
):
    """Renderiza o componente de formalização de descrição."""
    
    # Inicializa estado se necessário
    state_key = f"{key_prefix}_formalization" if key_prefix else "formalization"
    if state_key not in st.session_state:
        st.session_state[state_key] = {
            'formal_version': None,
            'changes': None,
            'terms': None,
            'show_preview': False
        }
    
    # Container para o botão de formalização
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🎩 Formalizar", 
                    disabled=not current_description,
                    key=f"{state_key}_formalize_btn"):
            with st.spinner("Formalizando descrição..."):
                try:
                    ai_service = AIService()
                    result = ai_service.formalize_description(current_description)
                    
                    # Atualiza o estado
                    st.session_state[state_key] = {
                        'formal_version': result['formal_description'],
                        'changes': result['changes_made'],
                        'terms': result['technical_terms'],
                        'show_preview': True
                    }
                    
                    st.success("Descrição formalizada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao formalizar descrição: {str(e)}")
    
    # Mostra preview se houver uma versão formalizada
    if st.session_state[state_key]['show_preview']:
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("##### Versão Original")
            st.text_area(
                "Original:",
                value=current_description,
                disabled=True,
                height=200,
                key=f"{state_key}_original"
            )
        
        with col2:
            st.write("##### Versão Formalizada")
            formal_text = st.text_area(
                "Formalizada:",
                value=st.session_state[state_key]['formal_version'],
                height=200,
                key=f"{state_key}_formal"
            )
        
        # Mostra alterações e termos técnicos
        with st.expander("📝 Detalhes das Alterações"):
            st.write("**Principais Mudanças:**")
            for change in st.session_state[state_key]['changes']:
                st.write(f"- {change}")
            
            st.write("\n**Termos Técnicos:**")
            st.write(", ".join(st.session_state[state_key]['terms']))
        
        # Botões de ação
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            if st.button("✅ Aceitar", key=f"{state_key}_accept_btn"):
                on_update(formal_text)
                st.session_state[state_key] = {
                    'formal_version': None,
                    'changes': None,
                    'terms': None,
                    'show_preview': False
                }
                st.success("Descrição atualizada!")
                st.rerun()
        
        with col2:
            if st.button("❌ Descartar", key=f"{state_key}_discard_btn"):
                st.session_state[state_key] = {
                    'formal_version': None,
                    'changes': None,
                    'terms': None,
                    'show_preview': False
                }
                st.rerun() 