import streamlit as st
from src.utils import logger
from src.controllers.process_controller import ProcessController
from src.views.components.process_form import (
    render_process_identification,
    render_process_details,
    render_business_rules,
    render_automation_goals
)

# Configuração da página
st.set_page_config(
    page_title="Agente Analista de RPA",
    page_icon="🤖",
    layout="wide"
)

# Inicialização do estado
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'step': 0,
        'controller': ProcessController(),
        'form_data': {},
    }

def get_state(key, default=None):
    return st.session_state.app_state.get(key, default)

def set_state(key, value):
    st.session_state.app_state[key] = value

def handle_form_submit(data: dict):
    """Processa o envio do formulário."""
    try:
        controller = get_state('controller')
        current_process = controller.get_current_process()
        
        if current_process:
            updated_data = current_process.to_dict()
            updated_data.update(data)
            controller.update_process(updated_data)
        else:
            controller.create_process(data)
        
        # Atualiza os dados do formulário
        form_data = get_state('form_data', {})
        form_data[get_state('step')] = data
        set_state('form_data', form_data)
        
        # Avança para próxima etapa
        set_state('step', get_state('step') + 1)
        return True
        
    except Exception as e:
        logger.error(f"Erro ao processar formulário: {e}")
        st.error(f"Erro ao processar formulário: {str(e)}")
        return False

def render_navigation():
    """Renderiza a navegação entre etapas."""
    steps = ["Identificação", "Detalhes", "Regras", "Objetivos"]
    current_step = get_state('step')
    
    cols = st.columns([1, 4, 1])
    
    # Botão Voltar
    with cols[0]:
        if current_step > 0:
            if st.button("← Voltar"):
                set_state('step', current_step - 1)
                st.experimental_rerun()
    
    # Progresso
    with cols[1]:
        st.progress(current_step / len(steps))
        st.write(f"Etapa atual: {steps[current_step]}")

def render_current_step():
    """Renderiza o formulário da etapa atual."""
    current_step = get_state('step')
    form_data = get_state('form_data', {})
    current_data = form_data.get(current_step, {})
    
    if current_step == 0:
        st.header("Identificação do Processo")
        render_process_identification(handle_form_submit, current_data)
    elif current_step == 1:
        st.header("Detalhamento do Processo Atual (As-Is)")
        render_process_details(handle_form_submit, current_data)
    elif current_step == 2:
        st.header("Regras de Negócio e Exceções")
        render_business_rules(handle_form_submit, current_data)
    elif current_step == 3:
        st.header("Objetivos da Automação e KPIs")
        render_automation_goals(handle_form_submit, current_data)
    elif current_step >= 4:
        render_pdd_preview()

def render_pdd_preview():
    """Renderiza a prévia do PDD."""
    st.success("Todas as informações foram coletadas!")
    process = get_state('controller').get_current_process()
    
    if process:
        st.header("Documento PDD Gerado")
        st.markdown("## Process Definition Document (PDD)")
        
        with st.expander("1. Informações do Processo", expanded=True):
            st.write(f"**Nome do Processo:** {process.name}")
            st.write(f"**Responsável:** {process.owner}")
            st.write(f"**Descrição:** {process.description}")
        
        with st.expander("2. Detalhes do Processo", expanded=True):
            st.write("**Passos do Processo:**")
            st.write(process.steps_as_is)
            st.write("**Sistemas/Ferramentas:**")
            st.write(process.systems)
            st.write("**Dados Utilizados:**")
            st.write(process.data_used)
        
        with st.expander("3. Regras e Exceções", expanded=True):
            st.write("**Regras de Negócio:**")
            st.write(process.business_rules)
            st.write("**Exceções:**")
            st.write(process.exceptions)
        
        with st.expander("4. Objetivos e KPIs", expanded=True):
            st.write("**Objetivos da Automação:**")
            st.write(process.automation_goals)
            st.write("**KPIs:**")
            st.write(process.kpis)

def main():
    """Função principal da aplicação."""
    st.title("Agente Analista de RPA")
    st.write("Este agente irá guiá-lo na coleta de informações para criação de um documento PDD.")
    
    render_navigation()
    render_current_step()

if __name__ == "__main__":
    main()
