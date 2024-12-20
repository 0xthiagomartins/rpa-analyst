import streamlit as st
from typing import Callable, Optional, List
from utils.validators import FormValidator

def validate_and_submit(data: dict, required_fields: List[str], on_submit: Callable) -> bool:
    """Valida os dados e submete o formulário se válido."""
    validator = FormValidator()
    is_valid, missing_fields = validator.validate_required_fields(data, required_fields)
    
    if not is_valid:
        missing_labels = [validator.get_field_label(field) for field in missing_fields]
        st.error(f"Por favor, preencha os campos obrigatórios: {', '.join(missing_labels)}")
        return False
    
    on_submit(data)
    return True

def render_process_identification(on_submit: Optional[Callable] = None):
    """Renderiza o formulário de identificação do processo."""
    with st.form("process_info"):
        process_name = st.text_input("Nome do processo: *")
        process_owner = st.text_input("Responsável pelo processo (Owner): *")
        process_description = st.text_area(
            "Descrição do processo: *",
            help="Descreva brevemente o objetivo do processo e seu contexto."
        )

        submitted = st.form_submit_button("Salvar informações do Processo")
        if submitted:
            data = {
                "process_name": process_name,
                "process_owner": process_owner,
                "process_description": process_description
            }
            required_fields = ["process_name", "process_owner", "process_description"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Informações do processo salvas com sucesso!")

def render_process_details(on_submit: Optional[Callable] = None):
    """Renderiza o formulário de detalhes do processo."""
    with st.form("as_is_form"):
        st.write("Quais são as etapas atuais do processo?")
        steps = st.text_area(
            "Passos do Processo (As-Is): *",
            help="Liste as etapas na ordem em que ocorrem."
        )
        
        systems = st.text_input(
            "Sistemas / Ferramentas: *",
            help="Ex: ERP SAP, CRM Salesforce, Excel..."
        )

        data_used = st.text_area(
            "Dados utilizados/produzidos: *",
            help="Ex: Dados cadastrais, registros de estoque..."
        )
        
        submitted = st.form_submit_button("Salvar detalhes (As-Is)")
        if submitted:
            data = {
                "steps_as_is": steps,
                "systems": systems,
                "data_used": data_used
            }
            required_fields = ["steps_as_is", "systems", "data_used"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Detalhes do processo atual salvos!")

def render_business_rules(on_submit: Optional[Callable] = None):
    """Renderiza o formulário de regras de negócio e exceções."""
    with st.form("rules_exceptions_form"):
        st.write("Identifique as regras de negócio que governam as decisões dentro do processo.")
        business_rules = st.text_area(
            "Regras de Negócio: *",
            help="Ex: Se valor > X, requer aprovação; Se campo vazio, notificar..."
        )

        st.write("Quais são as exceções ou condições atípicas que podem ocorrer?")
        exceptions = st.text_area(
            "Exceções e Erros Potenciais: *",
            help="Ex: Sistema fora do ar, dados incompletos, falha de autenticação..."
        )
        
        submitted = st.form_submit_button("Salvar Regras e Exceções")
        if submitted:
            data = {
                "business_rules": business_rules,
                "exceptions": exceptions
            }
            required_fields = ["business_rules", "exceptions"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Regras de negócio e exceções salvas!")

def render_automation_goals(on_submit: Optional[Callable] = None):
    """Renderiza o formulário de objetivos da automação e KPIs."""
    with st.form("goals_kpis_form"):
        st.write("O que se espera alcançar com a automação deste processo?")
        automation_goals = st.text_area(
            "Objetivos da Automação: *",
            help="Ex: Reduzir tempo de execução, diminuir erros manuais..."
        )
        
        st.write("Como será medido o sucesso da automação?")
        kpis = st.text_area(
            "KPIs/Indicadores de Sucesso: *",
            help="Ex: Tempo médio de execução, taxa de erros, volume processado..."
        )
        
        submitted = st.form_submit_button("Salvar Objetivos e KPIs")
        if submitted:
            data = {
                "automation_goals": automation_goals,
                "kpis": kpis
            }
            required_fields = ["automation_goals", "kpis"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Objetivos da automação e KPIs salvos!")