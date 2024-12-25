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
    # Usa dados salvos anteriormente ou dados iniciais
    saved_data = st.session_state.form_data.get('identification', {})
    initial_data = saved_data or initial_data or {}
    
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
            save = st.form_submit_button(
                "💾 Salvar",
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
    if save:
        data = {
            "process_name": process_name,
            "process_owner": process_owner,
            "process_description": description
        }
        required_fields = ["process_name", "process_owner", "process_description"]
        if validate_and_submit(data, required_fields, on_submit):
            # Analisa a descrição e sugere valores
            try:
                with st.spinner("Analisando descrição..."):
                    ai_service = AIService()
                    suggestions = ai_service.analyze_process_description(description)
                    
                    # Armazena sugestões no estado da sessão
                    if 'ai_suggestions' not in st.session_state:
                        st.session_state.ai_suggestions = {}
                    
                    st.session_state.ai_suggestions = suggestions
                    
                    # Mostra preview das sugestões
                    with st.expander("🤖 Sugestões da IA", expanded=True):
                        st.info("Com base na descrição, foram identificados os seguintes elementos:")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Etapas Identificadas:**")
                            for step in suggestions['details']['steps']:
                                st.write(f"• {step}")
                            
                            st.write("**Sistemas/Ferramentas:**")
                            for tool in suggestions['details']['tools']:
                                st.write(f"• {tool}")
                        
                        with col2:
                            st.write("**Regras de Negócio:**")
                            for rule in suggestions['business_rules']['business_rules']:
                                st.write(f"• {rule}")
                            
                            st.write("**Objetivos:**")
                            for goal in suggestions['automation_goals']['automation_goals']:
                                st.write(f"• {goal}")
                        
                        # Botões para aceitar/rejeitar sugestões
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Usar Sugestões", use_container_width=True):
                                # Salva as sugestões no estado
                                st.session_state.ai_suggestions = suggestions
                                
                                # Atualiza o process_details com as sugestões
                                if 'process_details' not in st.session_state:
                                    st.session_state.process_details = {
                                        'custom_tools': [],
                                        'custom_steps': [],
                                        'selected_tab': 'steps',
                                        'saved_steps': suggestions['details']['steps'],
                                        'saved_tools': suggestions['details']['tools']
                                    }
                                else:
                                    st.session_state.process_details.update({
                                        'saved_steps': suggestions['details']['steps'],
                                        'saved_tools': suggestions['details']['tools']
                                    })
                                
                                # Atualiza o form_data
                                st.session_state.form_data['details'] = suggestions['details']
                                st.session_state.form_data['business_rules'] = suggestions['business_rules']
                                st.session_state.form_data['automation_goals'] = suggestions['automation_goals']
                                
                                st.success("Sugestões aplicadas! Você pode revisar e ajustar nos próximos passos.")
                                st.rerun()
                        with col2:
                            if st.button("❌ Ignorar Sugestões", use_container_width=True):
                                st.session_state.ai_suggestions = {}
                                st.info("Sugestões ignoradas. Continue o preenchimento normalmente.")
                
            except Exception as e:
                st.error(f"Erro ao analisar descrição: {str(e)}")
            
            st.success("Informações salvas com sucesso!")

def render_process_details(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de detalhes do processo."""
    # Garante que form_data existe
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Pega os dados salvos - AQUI ESTÁ O PROBLEMA
    saved_data = st.session_state.form_data.get('details', {})
    
    # Se não tiver dados salvos mas tiver sugestões, usa as sugestões
    if not saved_data and 'ai_suggestions' in st.session_state:
        saved_data = st.session_state.ai_suggestions.get('details', {})
    
    # Processa as sugestões separando em padrão e customizado
    if saved_data:
        suggested_steps = saved_data.get('steps', [])
        suggested_tools = saved_data.get('tools', [])
        
        # Separa os steps em padrão e customizado
        standard_steps = [step for step in suggested_steps if step in OPTIONS['common_steps']]
        custom_steps = [step for step in suggested_steps if step not in OPTIONS['common_steps']]
        
        # Separa as ferramentas em padrão e customizado
        all_standard_tools = [tool for tools in OPTIONS['systems'].values() if isinstance(tools, list) for tool in tools]
        standard_tools = [tool for tool in suggested_tools if tool in all_standard_tools]
        custom_tools = [{'name': tool, 'type': 'Sistema'} 
                       for tool in suggested_tools 
                       if tool not in all_standard_tools]
        
        # Atualiza o estado com as sugestões
        if 'process_details' not in st.session_state:
            st.session_state.process_details = {
                'custom_tools': custom_tools,
                'custom_steps': custom_steps,
                'selected_tab': 'steps',
                'saved_steps': standard_steps,
                'saved_tools': standard_tools
            }
        else:
            st.session_state.process_details.update({
                'custom_tools': custom_tools,
                'custom_steps': custom_steps,
                'saved_steps': standard_steps,
                'saved_tools': standard_tools
            })
    
    # Debug para verificar os dados processados
    st.write("Debug - Dados Processados:", {
        'standard_steps': st.session_state.process_details.get('saved_steps', []),
        'custom_steps': st.session_state.process_details.get('custom_steps', []),
        'standard_tools': st.session_state.process_details.get('saved_tools', []),
        'custom_tools': st.session_state.process_details.get('custom_tools', [])
    })
    
    # Tabs para organizar as seções
    tab_steps, tab_tools, tab_data = st.tabs([
        "📝 Etapas do Processo",
        "🔧 Sistemas e Ferramentas",
        "📊 Dados Utilizados"
    ])
    
    with tab_steps:
        st.write("### Etapas do Processo")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Etapas Customizadas**")
            for idx, step in enumerate(st.session_state.process_details['custom_steps']):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.info(f"• {step}")
                with col_b:
                    if st.button("🗑️", key=f"btn_remove_step_{idx}_{step}"):
                        st.session_state.process_details['custom_steps'].remove(step)
                        st.rerun()
        
        with col2:
            st.write("**Adicionar Nova Etapa**")
            new_step = st.text_input("", placeholder="Digite uma nova etapa", key="new_step")
            if st.button("➕ Adicionar", key=f"btn_add_step_{new_step}"):
                if new_step and new_step not in st.session_state.process_details['custom_steps']:
                    st.session_state.process_details['custom_steps'].append(new_step)
                    st.rerun()
    
    with tab_tools:
        st.write("### Sistemas e Ferramentas")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Ferramentas Customizadas**")
            for idx, tool in enumerate(st.session_state.process_details['custom_tools']):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.info(f"• {tool['name']} ({tool['type']})")
                with col_b:
                    if st.button("🗑️", key=f"btn_remove_tool_{idx}_{tool['name']}"):
                        st.session_state.process_details['custom_tools'].remove(tool)
                        st.rerun()
        
        with col2:
            st.write("**Adicionar Nova Ferramenta**")
            new_tool = st.text_input("", placeholder="Nome da ferramenta", key="new_tool")
            tool_type = st.selectbox(
                "",
                ["Sistema", "Aplicativo", "Website", "API", "Outro"],
                key="new_tool_type"
            )
            if st.button("➕ Adicionar", key=f"btn_add_tool_{new_tool}"):
                if new_tool and not any(t['name'] == new_tool for t in st.session_state.process_details['custom_tools']):
                    st.session_state.process_details['custom_tools'].append({
                        'name': new_tool,
                        'type': tool_type
                    })
                    st.rerun()
    
    # Formulário principal
    with st.form("details_form", clear_on_submit=False):
        with tab_steps:
            st.write("**Etapas Comuns**")
            selected_steps = []
            
            # Debug para ver os steps que deveriam estar selecionados
            st.write("Debug - Steps para selecionar:", st.session_state.process_details['saved_steps'])
            
            for step in OPTIONS['common_steps']:
                is_selected = step in st.session_state.process_details['saved_steps']
                if st.checkbox(step, 
                             key=f"step_{step}",
                             value=is_selected):
                    selected_steps.append(step)
            
            # Adiciona etapas customizadas
            selected_steps.extend(st.session_state.process_details['custom_steps'])
        
        with tab_tools:
            st.write("**Sistemas e Ferramentas Comuns**")
            selected_systems = []
            
            # Agrupa ferramentas por categoria
            for category, tools in OPTIONS['systems'].items():
                if isinstance(tools, list):
                    st.write(f"**{category.replace('_', ' ').title()}:**")
                    for system in tools:
                        # Verifica se a ferramenta está nas sugestões salvas
                        is_selected = (system in st.session_state.process_details.get('saved_tools', []))
                        if st.checkbox(system, 
                                     key=f"system_{system}",
                                     value=is_selected):  # Usa o valor salvo
                            selected_systems.append(system)
            
            # Adiciona ferramentas customizadas
            selected_systems.extend([t['name'] for t in st.session_state.process_details.get('custom_tools', [])])
        
        with tab_data:
            st.write("### Dados do Processo")
            col1, col2 = st.columns(2)
            
            with col1:
                data_types = st.multiselect(
                    "Tipos de Dados:",
                    OPTIONS['data_types'],
                    default=initial_data.get('data_types', []),
                    key="data_types"
                )
                
                data_formats = st.multiselect(
                    "Formatos:",
                    ["Excel", "CSV", "PDF", "Texto", "Imagem", "Base de Dados"],
                    default=initial_data.get('data_formats', []),
                    key="data_formats"
                )
            
            with col2:
                data_sources = st.multiselect(
                    "Origens:",
                    ["Sistema Interno", "Planilha", "Email", "API", "Outro"],
                    default=initial_data.get('data_sources', []),
                    key="data_sources"
                )
                
                data_volume = st.select_slider(
                    "Volume:",
                    options=["Baixo", "Médio", "Alto", "Muito Alto"],
                    value=initial_data.get('data_volume', "Médio"),
                    key="data_volume"
                )
        
        # Botão de Salvar
        if st.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
            data = {
                "steps": selected_steps + st.session_state.process_details['custom_steps'],
                "tools": selected_systems + [t['name'] for t in st.session_state.process_details['custom_tools']],
                "data_types": data_types,
                "data_formats": data_formats,
                "data_sources": data_sources,
                "data_volume": data_volume
            }
            if validate_and_submit(data, ["steps", "tools"], on_submit):
                st.success("Detalhes do processo salvos com sucesso!")

def render_business_rules(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de regras de negócio e exceções."""
    # Usa dados salvos anteriormente ou dados iniciais
    saved_data = st.session_state.form_data.get('business_rules', {})
    
    # Se não tiver dados salvos mas tiver sugestões, usa as sugestões
    if not saved_data and 'ai_suggestions' in st.session_state:
        saved_data = st.session_state.ai_suggestions.get('business_rules', {})
    
    # Processa as sugestões separando em padrão e customizado
    if saved_data:
        suggested_rules = saved_data.get('business_rules', [])
        suggested_exceptions = saved_data.get('exceptions', [])
        
        # Separa as regras em padrão e customizado
        standard_rules = [rule for rule in suggested_rules if rule in OPTIONS.get('business_rules_templates', [])]
        custom_rules = [rule for rule in suggested_rules if rule not in OPTIONS.get('business_rules_templates', [])]
        
        # Separa as exceções em padrão e customizado
        standard_exceptions = [exc for exc in suggested_exceptions if exc in OPTIONS.get('common_exceptions', [])]
        custom_exceptions = [exc for exc in suggested_exceptions if exc not in OPTIONS.get('common_exceptions', [])]
        
        # Atualiza o estado com as sugestões
        if 'business_rules' not in st.session_state:
            st.session_state.business_rules = {
                'selected_rules': standard_rules,
                'custom_rules': '\n'.join(custom_rules),
                'selected_exceptions': standard_exceptions,
                'custom_exceptions': '\n'.join(custom_exceptions)
            }
        else:
            st.session_state.business_rules.update({
                'selected_rules': standard_rules,
                'custom_rules': '\n'.join(custom_rules),
                'selected_exceptions': standard_exceptions,
                'custom_exceptions': '\n'.join(custom_exceptions)
            })
    
    # Debug para verificar os dados processados
    st.write("Debug - Dados Processados:", {
        'saved_data': saved_data,
        'business_rules_state': st.session_state.business_rules
    })
    
    with st.form("rules_form", clear_on_submit=False):
        st.write("### Regras de Negócio")
        
        # Templates de regras comuns
        selected_rules = st.multiselect(
            "Selecione as regras aplicáveis:",
            OPTIONS.get('business_rules_templates', []),
            default=st.session_state.business_rules.get('selected_rules', [])
        )
        
        # Editor de regras customizadas
        st.write("Adicione ou edite regras específicas:")
        custom_rules = st.text_area(
            "Regras customizadas",
            value=st.session_state.business_rules.get('custom_rules', ''),
            help="Digite uma regra por linha",
            height=150
        )
        
        st.write("### Exceções e Tratamentos")
        
        # Exceções comuns
        selected_exceptions = st.multiselect(
            "Selecione as exceções possíveis:",
            OPTIONS.get('common_exceptions', []),
            default=st.session_state.business_rules.get('selected_exceptions', [])
        )
        
        # Exceções customizadas
        custom_exceptions = st.text_area(
            "Adicione outras exceções específicas:",
            value=st.session_state.business_rules.get('custom_exceptions', ''),
            help="Digite uma exceção por linha",
            height=150
        )
        
        # Botão de Salvar
        if st.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
            # Atualiza o estado
            st.session_state.business_rules.update({
                'selected_rules': selected_rules,
                'custom_rules': custom_rules,
                'selected_exceptions': selected_exceptions,
                'custom_exceptions': custom_exceptions
            })
            
            # Prepara dados para submissão
            all_rules = selected_rules + [rule for rule in custom_rules.split('\n') if rule.strip()]
            all_exceptions = selected_exceptions + [exc for exc in custom_exceptions.split('\n') if exc.strip()]
            
            data = {
                "business_rules": all_rules,
                "exceptions": all_exceptions
            }
            
            if validate_and_submit(data, ["business_rules", "exceptions"], on_submit):
                st.success("Regras e exceções salvas com sucesso!")

def render_automation_goals(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de objetivos da automação e KPIs."""
    # Usa dados salvos anteriormente ou dados iniciais
    saved_data = st.session_state.form_data.get('automation_goals', {})
    
    # Se não tiver dados salvos mas tiver sugestões, usa as sugestões
    if not saved_data and 'ai_suggestions' in st.session_state:
        saved_data = st.session_state.ai_suggestions.get('automation_goals', {})
    
    # Processa as sugestões separando em padrão e customizado
    if saved_data:
        suggested_goals = saved_data.get('automation_goals', [])
        suggested_kpis = saved_data.get('kpis', [])
        
        # Separa os objetivos em padrão e customizado
        standard_goals = [goal for goal in suggested_goals if goal in OPTIONS.get('automation_goals', [])]
        custom_goals = [goal for goal in suggested_goals if goal not in OPTIONS.get('automation_goals', [])]
        
        # Separa os KPIs em padrão e customizado
        standard_kpis = [kpi for kpi in suggested_kpis if kpi in OPTIONS.get('kpi_templates', [])]
        custom_kpis = [kpi for kpi in suggested_kpis if kpi not in OPTIONS.get('kpi_templates', [])]
        
        # Atualiza o estado com as sugestões
        if 'automation_goals' not in st.session_state:
            st.session_state.automation_goals = {
                'selected_goals': standard_goals,
                'custom_goals': '\n'.join(custom_goals),
                'selected_kpis': standard_kpis,
                'custom_kpis': '\n'.join(custom_kpis)
            }
        else:
            st.session_state.automation_goals.update({
                'selected_goals': standard_goals,
                'custom_goals': '\n'.join(custom_goals),
                'selected_kpis': standard_kpis,
                'custom_kpis': '\n'.join(custom_kpis)
            })
    
    # Debug para verificar os dados processados
    st.write("Debug - Dados Processados:", {
        'saved_data': saved_data,
        'automation_goals_state': st.session_state.get('automation_goals', {})
    })
    
    with st.form("goals_form", clear_on_submit=False):
        st.write("### Objetivos da Automação")
        
        # Seleção de objetivos comuns
        selected_goals = st.multiselect(
            "Selecione os objetivos da automação:",
            OPTIONS['automation_goals'],
            default=st.session_state.get('automation_goals', {}).get('selected_goals', [])
        )
        
        # Objetivos customizados
        custom_goals = st.text_area(
            "Adicione outros objetivos específicos:",
            value=st.session_state.get('automation_goals', {}).get('custom_goals', ''),
            help="Digite um objetivo por linha"
        )
        
        st.write("### KPIs e Métricas")
        
        # Seleção de KPIs comuns
        selected_kpis = st.multiselect(
            "Selecione os KPIs aplicáveis:",
            OPTIONS['kpi_templates'],
            default=st.session_state.get('automation_goals', {}).get('selected_kpis', [])
        )
        
        # KPIs customizados
        custom_kpis = st.text_area(
            "Adicione outros KPIs específicos:",
            value=st.session_state.get('automation_goals', {}).get('custom_kpis', ''),
            help="Digite um KPI por linha"
        )
        
        # Botão de Salvar
        if st.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
            # Atualiza o estado
            st.session_state.automation_goals = {
                'selected_goals': selected_goals,
                'custom_goals': custom_goals,
                'selected_kpis': selected_kpis,
                'custom_kpis': custom_kpis
            }
            
            # Prepara dados para submissão
            all_goals = selected_goals + [goal for goal in custom_goals.split('\n') if goal.strip()]
            all_kpis = selected_kpis + [kpi for kpi in custom_kpis.split('\n') if kpi.strip()]
            
            data = {
                "automation_goals": all_goals,
                "kpis": all_kpis
            }
            
            if validate_and_submit(data, ["automation_goals", "kpis"], on_submit):
                st.success("Objetivos e KPIs salvos com sucesso!")