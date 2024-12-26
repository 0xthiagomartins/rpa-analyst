import streamlit as st

# Configuração da página DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Agente Analista de RPA",
    page_icon="🤖",
    layout="wide"
)

from src.views.components.process_form import (
    render_process_identification,
    render_process_details,
    render_business_rules,
    render_automation_goals
)
from src.views.components.process_diagram import render_process_diagram
from src.services.document_service import DocumentService
import os

STEPS = {
    "identification": ("Identificação do Processo", render_process_identification),
    "details": ("Detalhes do Processo", render_process_details),
    "business_rules": ("Regras de Negócio", render_business_rules),
    "automation_goals": ("Objetivos e KPIs", render_automation_goals)
}

def init_session_state():
    """Inicializa o estado da sessão."""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "identification"
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    if 'process_details' not in st.session_state:
        st.session_state.process_details = {
            'custom_tools': [],
            'custom_steps': [],
            'selected_tab': 'steps',
            'saved_steps': [],
            'saved_tools': []
        }

def calculate_progress():
    """Calcula o progresso baseado na posição atual e dados preenchidos."""
    if not st.session_state.form_data:
        return 0.0
    
    # Define a ordem dos steps
    step_order = ["identification", "details", "business_rules", "automation_goals"]
    current_index = step_order.index(st.session_state.current_step)
    
    # Conta steps preenchidos até o atual
    completed_steps = sum(1 for step in step_order[:current_index + 1] 
                         if step in st.session_state.form_data)
    
    # Calcula progresso baseado na posição atual
    total_steps = len(step_order)
    base_progress = (current_index + 1) / total_steps
    completion_progress = completed_steps / total_steps
    
    # Retorna o menor valor entre a posição atual e os steps completados
    return min(base_progress, completion_progress)

def render_navigation():
    """Renderiza a navegação entre etapas e barra de progresso."""
    # Barra de progresso
    progress = calculate_progress()
    st.progress(progress)
    
    # Indicador de progresso em texto
    current_step = list(STEPS.keys()).index(st.session_state.current_step) + 1
    total_steps = len(STEPS)
    progress_text = f"Etapa {current_step} de {total_steps}"
    st.caption(progress_text)
    
    # Navegação visual (sem botões)
    steps = list(STEPS.items())
    cols = st.columns(len(steps))
    for idx, (step_key, (title, _)) in enumerate(steps):
        with cols[idx]:
            if step_key == st.session_state.current_step:
                st.markdown(f"**✏️ {title}**")
            elif step_key in st.session_state.form_data:
                st.markdown(f"✅ {title}")
            else:
                st.markdown(f"⭕ {title}")

def render_step_navigation():
    """Renderiza botões de navegação entre steps."""
    step_order = ["identification", "details", "business_rules", "automation_goals"]
    current_index = step_order.index(st.session_state.current_step)
    
    # Layout com 2 colunas para os botões de navegação
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Botão Voltar
        if current_index > 0:
            if st.button("← Voltar", 
                        key="btn_step_back",
                        use_container_width=True):
                st.session_state.current_step = step_order[current_index - 1]
                st.rerun()
    
    with col2:
        # Botão Avançar (habilitado apenas se o step atual estiver salvo)
        if current_index < len(step_order) - 1:
            next_disabled = st.session_state.current_step not in st.session_state.form_data
            if st.button("Avançar →", 
                        key="btn_step_next",
                        disabled=next_disabled,
                        type="primary",
                        use_container_width=True):
                st.session_state.current_step = step_order[current_index + 1]
                st.rerun()
            
            # Mostra mensagem se o botão estiver desabilitado
            if next_disabled:
                st.caption("💡 Salve os dados para avançar")

def handle_form_submit(data: dict):
    """Manipula o envio do formulário."""
    # Salva os dados do passo atual
    st.session_state.form_data[st.session_state.current_step] = data
    return True  # Removido o avanço automático

def can_generate_pdd() -> bool:
    """Verifica se todos os dados necessários estão preenchidos."""
    required_steps = ["identification", "details", "business_rules", "automation_goals"]
    return all(step in st.session_state.form_data for step in required_steps)

def prepare_pdd_data() -> dict:
    """Prepara os dados para geração do PDD."""
    form_data = st.session_state.form_data
    
    # Mapeia os dados do formulário para o formato esperado pelo DocumentService
    pdd_data = {
        # Dados de identificação
        "process_name": form_data["identification"].get("process_name", ""),
        "process_owner": form_data["identification"].get("process_owner", ""),
        "process_description": form_data["identification"].get("process_description", ""),
        
        # Dados de detalhes do processo
        "steps_as_is": form_data["details"].get("steps", []),
        "systems": form_data["details"].get("tools", []),
        "data_used": {
            "types": form_data["details"].get("data_types", []),
            "formats": form_data["details"].get("data_formats", []),
            "sources": form_data["details"].get("data_sources", []),
            "volume": form_data["details"].get("data_volume", "Médio")
        },
        
        # Regras de negócio e exceções
        "business_rules": form_data["business_rules"].get("business_rules", []),
        "exceptions": form_data["business_rules"].get("exceptions", []),
        
        # Objetivos e KPIs
        "automation_goals": form_data["automation_goals"].get("automation_goals", ""),
        "kpis": form_data["automation_goals"].get("kpis", ""),
        
        # Adiciona o código do diagrama se existir
        "diagram_code": st.session_state.get('diagram_code', None)
    }
    
    return pdd_data

def render_current_step():
    """Renderiza o passo atual do formulário."""
    # Inicializa o estado se necessário
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "identification"
    
    # Carrega dados iniciais se existirem
    initial_data = {}
    if 'form_data' in st.session_state:
        initial_data = st.session_state.form_data.get(st.session_state.current_step, {})
    
    # Renderiza o título do passo atual
    current_title, render_form = STEPS[st.session_state.current_step]
    st.header(current_title)
    
    # Renderiza o formulário do passo atual
    render_form(on_submit=handle_form_submit, initial_data=initial_data)
    
    # Renderiza navegação entre steps
    st.divider()
    render_step_navigation()
    
    # Adiciona o diagrama após preencher todos os dados
    if all(step in st.session_state.form_data for step in ["identification", "details", "business_rules", "automation_goals"]):
        st.divider()
        render_process_diagram(prepare_pdd_data())
    
    # Botão de geração do PDD (apenas no último passo)
    if st.session_state.current_step == "automation_goals" and can_generate_pdd():
        st.divider()
        st.write("### 📄 Geração do Documento")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🚀 Gerar PDD", 
                        type="primary", 
                        use_container_width=True,
                        key="btn_generate_pdd"):
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
                            use_container_width=True,
                            key="btn_download_pdd"
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar PDD: {str(e)}")

def main():
    """Função principal da aplicação."""
    init_session_state()
    
    st.title("🤖 Agente Analista de RPA")
    st.write("Assistente para criação de documentos PDD para automação RPA")
    
    render_navigation()
    
    # Separador visual
    st.divider()
    
    render_current_step()

if __name__ == "__main__":
    main()
