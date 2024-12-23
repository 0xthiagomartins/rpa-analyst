import streamlit as st
from src.views.components.process_form import (
    render_process_identification,
    render_process_details,
    render_business_rules,
    render_automation_goals
)
from src.services.document_service import DocumentService
import os

STEPS = {
    0: ("Identificação", render_process_identification),
    1: ("Detalhes do Processo", render_process_details),
    2: ("Regras de Negócio", render_business_rules),
    3: ("Objetivos da Automação", render_automation_goals)
}

def init_session_state():
    """Inicializa o estado da sessão."""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

def calculate_progress():
    """Calcula o progresso baseado nos dados preenchidos."""
    if not st.session_state.form_data:
        return 0.0
    
    steps_completed = len(st.session_state.form_data)
    return min(steps_completed / len(STEPS), 1.0)

def render_navigation():
    """Renderiza a navegação entre etapas e barra de progresso."""
    # Barra de progresso
    progress = calculate_progress()
    st.progress(progress)
    
    # Indicador de progresso em texto
    progress_text = f"Progresso: {int(progress * 100)}%"
    st.caption(progress_text)
    
    # Navegação
    cols = st.columns(len(STEPS))
    for idx, (title, _) in STEPS.items():
        with cols[idx]:
            if idx == st.session_state.current_step:
                st.markdown(f"**➡️ {title}**")
            elif idx in st.session_state.form_data:
                st.markdown(f"✅ {title}")
            else:
                st.markdown(f"⭕ {title}")

def handle_form_submit(data: dict):
    """Manipula o envio do formulário."""
    st.session_state.form_data[st.session_state.current_step] = data
    if st.session_state.current_step < len(STEPS) - 1:
        st.session_state.current_step += 1
    return True

def can_generate_pdd() -> bool:
    """Verifica se todos os dados necessários estão preenchidos."""
    return len(st.session_state.form_data) == len(STEPS)

def prepare_pdd_data() -> dict:
    """Prepara os dados para geração do PDD."""
    data = {}
    for step_data in st.session_state.form_data.values():
        data.update(step_data)
    return data

def render_current_step():
    """Renderiza o formulário da etapa atual."""
    # Título da etapa atual
    current_title, render_form = STEPS[st.session_state.current_step]
    st.header(current_title)
    
    # Botões de navegação
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.session_state.current_step > 0:
            if st.button("← Voltar"):
                st.session_state.current_step -= 1
                st.rerun()
    
    # Renderiza o formulário
    initial_data = st.session_state.form_data.get(st.session_state.current_step, {})
    render_form(on_submit=handle_form_submit, initial_data=initial_data)
    
    # Botão de geração do PDD
    if can_generate_pdd():
        st.divider()
        st.write("### 📄 Geração do Documento")
        if st.button("🚀 Gerar PDD", type="primary", use_container_width=True):
            try:
                with st.spinner("Gerando documento..."):
                    doc_service = DocumentService()
                    pdf_path = doc_service.generate_pdd(prepare_pdd_data())
                
                st.success("PDD gerado com sucesso!")
                
                # Oferece download do arquivo
                with open(pdf_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download PDD",
                        data=f.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar PDD: {str(e)}")

def main():
    """Função principal da aplicação."""
    st.set_page_config(
        page_title="Agente Analista de RPA",
        page_icon="🤖",
        layout="wide"
    )
    
    init_session_state()
    
    st.title("🤖 Agente Analista de RPA")
    st.write("Assistente para criação de documentos PDD para automação RPA")
    
    render_navigation()
    
    # Separador visual
    st.divider()
    
    render_current_step()

if __name__ == "__main__":
    main()
