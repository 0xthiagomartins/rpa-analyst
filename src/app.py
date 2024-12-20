import streamlit as st
from src.controllers.process_controller import ProcessController
from src.views.components.process_form import (
    render_process_identification,
    render_process_details,
    render_business_rules,
    render_automation_goals
)
from src.utils import AppContext

# Configuração da página
st.set_page_config(
    page_title="Agente Analista de RPA",
    page_icon="🤖",
    layout="wide"
)

# Inicialização do contexto
app_context = AppContext()
config = app_context.get_config()

# Inicialização do controlador
if 'process_controller' not in st.session_state:
    st.session_state.process_controller = ProcessController()

# Inicialização do estado de progresso
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

st.title("Agente Analista de RPA")
st.write("Este agente irá guiá-lo na coleta de informações para criação de um documento PDD.")

# Callbacks
def handle_form_submit(data: dict):
    controller = st.session_state.process_controller
    current_process = controller.get_current_process()
    
    if current_process:
        updated_data = current_process.to_dict()
        updated_data.update(data)
        controller.update_process(updated_data)
    else:
        controller.create_process(data)
    
    # Avança para o próximo passo
    st.session_state.current_step += 1

# Barra de progresso
steps = ["Identificação", "Detalhes", "Regras", "Objetivos"]
progress = st.progress(st.session_state.current_step / len(steps))
st.write(f"Etapa atual: {steps[st.session_state.current_step]}")

# Renderização dos formulários baseada no passo atual
if st.session_state.current_step == 0:
    st.header("Identificação do Processo")
    render_process_identification(handle_form_submit)

elif st.session_state.current_step == 1:
    st.header("Detalhamento do Processo Atual (As-Is)")
    render_process_details(handle_form_submit)

elif st.session_state.current_step == 2:
    st.header("Regras de Negócio e Exceções")
    render_business_rules(handle_form_submit)

elif st.session_state.current_step == 3:
    st.header("Objetivos da Automação e KPIs")
    render_automation_goals(handle_form_submit)

# Botão para voltar
if st.session_state.current_step > 0:
    if st.button("← Voltar"):
        st.session_state.current_step -= 1
        st.rerun()

# Exibição do PDD quando todas as etapas forem concluídas
if st.session_state.current_step >= len(steps):
    st.success("Todas as informações foram coletadas!")
    process = st.session_state.process_controller.get_current_process()
    
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
