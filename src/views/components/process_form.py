import yaml
from pathlib import Path
import streamlit as st
from typing import Callable, Optional, List
from src.utils.validators import FormValidator
from src.views.components.diagram_editor import render_diagram_editor
from .description_formalizer import render_description_formalizer
from src.services.ai_service import AIService
from streamlit_modal import Modal

def load_form_options():
    """Carrega as opções predefinidas do formulário."""
    config_path = Path(__file__).parent.parent.parent.parent / 'config' / 'form_options.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

OPTIONS = load_form_options()

def validate_and_submit(data: dict, required_fields: List[str], on_submit: Callable) -> bool:
    """Valida os dados e submete o formulário se válido."""
    if on_submit is None:
        st.error("Callback de submissão não fornecido")
        return False
        
    validator = FormValidator()
    is_valid, missing_fields = validator.validate_required_fields(data, required_fields)
    
    if not is_valid:
        missing_labels = [validator.get_field_label(field) for field in missing_fields]
        st.error(f"Por favor, preencha os campos obrigatórios: {', '.join(missing_labels)}")
        return False
    
    try:
        on_submit(data)
        return True
    except Exception as e:
        st.error(f"Erro ao submeter formulário: {str(e)}")
        return False

def render_process_identification(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de identificação do processo."""
    initial_data = initial_data or {}
    
    # Inicializa o estado se necessário
    if 'process_form' not in st.session_state:
        st.session_state.process_form = {
            'description': initial_data.get('description', ''),
            'formalized_text': None,
            'show_formalization': False
        }
    
    # Formulário principal
    with st.form("identification_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            process_name = st.text_input(
                "Nome do processo: *",
                value=initial_data.get('process_name', ''),
                placeholder="Ex: Processamento de Notas Fiscais"
            )
        
        with col2:
            process_owner = st.text_input(
                "Responsável pelo processo (Owner): *",
                value=initial_data.get('process_owner', ''),
                placeholder="Ex: João Silva"
            )
        
        # Campo de descrição único
        description = st.text_area(
            "Descrição do Processo",
            value=st.session_state.process_form['description'],
            help="Descreva o processo de forma detalhada",
            height=150,
            key="process_description"
        )
        
        # Botões em colunas
        col1, col2 = st.columns([1, 2])
        with col1:
            formalize = st.form_submit_button(
                "🎩 Formalizar",
                use_container_width=True
            )
        with col2:
            submit = st.form_submit_button(
                "Avançar →",
                use_container_width=True,
                type="primary"
            )
    
    # Lógica de formalização
    if formalize and description:
        with st.spinner("Formalizando descrição..."):
            try:
                ai_service = AIService()
                result = ai_service.formalize_description(description)
                st.session_state.process_form['formalized_text'] = result
                st.session_state.process_form['show_formalization'] = True
                
            except Exception as e:
                st.error(f"Erro ao formalizar descrição: {str(e)}")
    
    # Mostra a formalização se necessário
    if st.session_state.process_form['show_formalization']:
        with st.expander("🔄 Confirmar Formalização", expanded=True):
            formalized = st.session_state.process_form['formalized_text']['formal_description']
            
            # Comparação das versões
            st.write("#### Comparação das Versões")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Original:**\n" + description)
            with col2:
                st.success("**Formalizada:**\n" + formalized)
            
            # Detalhes
            st.write("**Principais Mudanças:**")
            for change in st.session_state.process_form['formalized_text']['changes_made']:
                st.write(f"- {change}")
            
            st.write("**Termos Técnicos:**")
            st.write(", ".join(st.session_state.process_form['formalized_text']['technical_terms']))
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Usar Versão Formalizada", use_container_width=True):
                    st.session_state.process_form['description'] = formalized
                    st.session_state.process_form['show_formalization'] = False
                    st.session_state.process_form['formalized_text'] = None
                    st.rerun()
            with col2:
                if st.button("❌ Manter Original", use_container_width=True):
                    st.session_state.process_form['show_formalization'] = False
                    st.session_state.process_form['formalized_text'] = None
                    st.rerun()
    
    # Lógica de submissão
    if submit:
        data = {
            "process_name": process_name,
            "process_owner": process_owner,
            "process_description": description
        }
        required_fields = ["process_name", "process_owner", "process_description"]
        if validate_and_submit(data, required_fields, on_submit):
            st.success("Informações salvas com sucesso!")

def render_process_details(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de detalhes do processo."""
    initial_data = initial_data or {}
    
    # Estado para gerenciar ferramentas customizadas
    if 'custom_tools' not in st.session_state:
        st.session_state.custom_tools = []
    
    # Área para adicionar nova ferramenta (fora do form)
    st.write("### Sistemas e Ferramentas")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_tool = st.text_input("Adicionar nova ferramenta:", key="new_tool_input")
    with col2:
        if st.button("Adicionar", key="add_tool_button"):
            if new_tool and new_tool not in st.session_state.custom_tools:
                st.session_state.custom_tools.append(new_tool)
                st.rerun()
    
    # Lista de ferramentas customizadas
    if st.session_state.custom_tools:
        st.write("Ferramentas adicionadas:")
        for tool in st.session_state.custom_tools:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(tool)
            with col2:
                if st.button("Remover", key=f"remove_{tool}"):
                    st.session_state.custom_tools.remove(tool)
                    st.rerun()
    
    # Formulário principal
    with st.form("as_is_form"):
        st.write("### Etapas do Processo")
        
        # Seleção de etapas comuns
        selected_steps = st.multiselect(
            "Selecione as etapas que fazem parte do processo:",
            OPTIONS['common_steps'],
            default=[]
        )
        
        # Campo para etapas adicionais
        custom_steps = st.text_area(
            "Adicione outras etapas específicas:",
            value=initial_data.get('custom_steps', ''),
            help="Digite uma etapa por linha"
        )
        
        st.write("### Sistemas e Ferramentas")
        
        # Seleção de ferramentas comuns + customizadas
        all_tools = OPTIONS['systems']['common_tools'] + st.session_state.custom_tools
        selected_tools = st.multiselect(
            "Selecione as ferramentas utilizadas:",
            all_tools,
            default=[]
        )
        
        st.write("### Dados Utilizados")
        
        # Seleção de tipos de dados comuns
        selected_data = st.multiselect(
            "Selecione os tipos de dados:",
            OPTIONS['data_types'],
            default=[]
        )
        
        # Campo para outros tipos de dados
        custom_data = st.text_area(
            "Especifique outros tipos de dados:",
            value=initial_data.get('custom_data', ''),
            help="Digite um tipo por linha"
        )
        
        if st.form_submit_button("Avançar →", use_container_width=True):
            # Combina etapas selecionadas e customizadas
            all_steps = selected_steps + [step for step in custom_steps.split('\n') if step.strip()]
            
            # Combina dados selecionados e customizados
            all_data = selected_data + [data for data in custom_data.split('\n') if data.strip()]
            
            data = {
                "steps_as_is": "\n".join(all_steps),
                "systems": ", ".join(selected_tools),
                "data_used": "\n".join(all_data)
            }
            
            # Validação específica para esta seção
            validator = FormValidator()
            errors = validator.validate_form(data, 'process_details')
            
            if errors:
                for error in errors:
                    st.error(error.message)
            else:
                if on_submit(data):
                    st.success("Detalhes do processo salvos com sucesso!")
                    # Limpa as ferramentas customizadas após salvar
                    st.session_state.custom_tools = []
    
    # Após o formulário principal, renderiza o editor de diagrama
    if st.session_state.get('form_data', {}).get(0):  # Se tiver dados da primeira etapa
        process_description = st.session_state.form_data[0].get('process_description', '')
        current_steps = [step for step in custom_steps.split('\n') if step.strip()]
        
        render_diagram_editor(process_description, current_steps)

def render_business_rules(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de regras de negócio e exceções."""
    initial_data = initial_data or {}
    
    with st.form("rules_form"):
        st.write("### Regras de Negócio")
        
        # Templates de regras comuns
        selected_rules = st.multiselect(
            "Selecione as regras aplicáveis:",
            OPTIONS['business_rules_templates'],
            default=[]
        )
        
        # Editor de regras customizadas
        st.write("Adicione ou edite regras específicas:")
        custom_rules = st.text_area(
            "Regras customizadas",
            value=initial_data.get('custom_rules', ''),
            help="Digite uma regra por linha"
        )
        
        st.write("### Exceções e Tratamentos")
        
        # Exceções comuns
        selected_exceptions = st.multiselect(
            "Selecione as exceções possíveis:",
            OPTIONS['common_exceptions'],
            default=[]
        )
        
        # Exceções customizadas
        custom_exceptions = st.text_area(
            "Adicione outras exceções específicas:",
            value=initial_data.get('custom_exceptions', ''),
            help="Digite uma exceção por linha"
        )
        
        if st.form_submit_button("Avançar →", use_container_width=True):
            # Combina regras selecionadas e customizadas
            all_rules = selected_rules + [rule for rule in custom_rules.split('\n') if rule.strip()]
            
            # Combina exceções selecionadas e customizadas
            all_exceptions = selected_exceptions + [exc for exc in custom_exceptions.split('\n') if exc.strip()]
            
            data = {
                "business_rules": "\n".join(all_rules),
                "exceptions": "\n".join(all_exceptions)
            }
            
            required_fields = ["business_rules", "exceptions"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Regras e exceções salvas com sucesso!")

def render_automation_goals(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de objetivos da automação e KPIs."""
    initial_data = initial_data or {}
    
    with st.form("goals_kpis_form"):
        st.write("### Objetivos da Automação")
        
        # Seleção de objetivos comuns
        selected_goals = st.multiselect(
            "Selecione os objetivos da automação:",
            OPTIONS['automation_goals'],
            default=[]
        )
        
        # Objetivos customizados
        custom_goals = st.text_area(
            "Adicione outros objetivos específicos:",
            value=initial_data.get('custom_goals', ''),
            help="Digite um objetivo por linha"
        )
        
        st.write("### KPIs e Métricas")
        
        # Seleção de KPIs comuns
        selected_kpis = st.multiselect(
            "Selecione os KPIs aplicáveis:",
            OPTIONS['kpi_templates'],
            default=[]
        )
        
        # KPIs customizados
        custom_kpis = st.text_area(
            "Adicione outros KPIs específicos:",
            value=initial_data.get('custom_kpis', ''),
            help="Digite um KPI por linha"
        )
        
        if st.form_submit_button("Finalizar", use_container_width=True):
            # Combina objetivos selecionados e customizados
            all_goals = selected_goals + [goal for goal in custom_goals.split('\n') if goal.strip()]
            
            # Combina KPIs selecionados e customizados
            all_kpis = selected_kpis + [kpi for kpi in custom_kpis.split('\n') if kpi.strip()]
            
            data = {
                "automation_goals": "\n".join(all_goals),
                "kpis": "\n".join(all_kpis)
            }
            
            required_fields = ["automation_goals", "kpis"]
            if validate_and_submit(data, required_fields, on_submit):
                st.success("Objetivos e KPIs salvos com sucesso!")