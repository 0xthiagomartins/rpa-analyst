import yaml
from pathlib import Path
import streamlit as st
from typing import Callable, Optional, List
from src.utils.validators import FormValidator
from src.views.components.diagram_editor import render_diagram_editor
from .description_formalizer import render_description_formalizer
from src.services.ai_service import AIService
from streamlit_modal import Modal
from streamlit_sortables import sort_items
from datetime import datetime

def get_default_options():
    """Retorna as opções padrão caso o arquivo de configuração não exista."""
    return {
        'common_tools': [
            'Microsoft Excel',
            'Microsoft Outlook',
            'SAP',
            'Power BI',
            'SharePoint',
            'Teams',
            'Oracle',
            'Salesforce',
            'ServiceNow',
            'Power Automate'
        ],
        'data_types': [
            'Dados financeiros',
            'Documentos fiscais',
            'Dados cadastrais',
            'Dados de controle',
            'Documentos digitalizados',
            'Planilhas',
            'Emails',
            'Relatórios',
            'Números de protocolo',
            'Valores monetários',
            'Dados de login',
            'Arquivos PDF'
        ],
        'data_formats': [
            'PDF',
            'Excel',
            'Word',
            'CSV',
            'TXT',
            'XML',
            'JSON',
            'Email',
            'Imagem',
            'Login',
            'Monetário'
        ],
        'data_sources': [
            'Email',
            'Sistema interno',
            'Portal web',
            'Pasta compartilhada',
            'Banco de dados',
            'API',
            'Planilha',
            'Scanner'
        ],
        'business_rules_templates': [
            'Validação de dados obrigatórios',
            'Verificação de duplicidade',
            'Aprovação por valor',
            'Verificação de prazo',
            'Validação de formato',
            'Checagem de permissões'
        ],
        'common_exceptions': [
            'Sistema indisponível',
            'Dados inconsistentes',
            'Arquivo corrompido',
            'Timeout de operação',
            'Erro de autenticação',
            'Permissão negada'
        ],
        'automation_goals': [
            'Redução de tempo de processamento',
            'Eliminação de erros manuais',
            'Padronização do processo',
            'Aumento de produtividade',
            'Melhoria da qualidade',
            'Redução de custos'
        ],
        'kpi_templates': [
            'Tempo médio de processamento',
            'Taxa de erro',
            'Volume processado',
            'Custo por transação',
            'Tempo de resposta',
            'Satisfação do usuário'
        ]
    }

def load_form_options():
    """Carrega as opções predefinidas do formulário."""
    try:
        config_path = Path(__file__).parent.parent.parent.parent / 'config' / 'form_options.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            options = yaml.safe_load(f)
        # Verifica se todas as chaves necessárias existem
        default_option = get_default_options()
        for key in default_option:
            if key not in options:
                options[key] = default_option[key]
                
        return options
    except Exception as e:
        st.warning(f"Erro ao carregar opções do arquivo: {str(e)}. Usando opções padrão.")
        return get_default_options()

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

def render_ai_suggestions_debug(suggestions: dict):
    """Renderiza uma seção de debug com todas as sugestões da IA."""
    st.markdown("""
    <style>
    .step-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        background-color: #f8f9fa;
    }
    .step-type {
        font-size: 0.8em;
        padding: 2px 8px;
        border-radius: 12px;
        margin-left: 8px;
        color: white;
    }
    .step-time {
        float: right;
        color: #666;
        font-size: 0.8em;
    }
    .step-description {
        color: #666;
        font-size: 0.9em;
        margin-top: 5px;
    }
    .step-dependencies {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
        border-top: 1px solid #eee;
        padding-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs para organizar a visualização
    tab1, tab2 = st.tabs(["📊 Visualização Formatada", "🔍 JSON Completo"])
    
    with tab1:
        # Etapas do Processo
        st.write("### 📝 Etapas do Processo")
        
        # Mapeamento de tipos para ícones e cores
        type_styles = {
            'start': {'icon': '🟢', 'color': '#28a745'},
            'action': {'icon': '▶️', 'color': '#007bff'},
            'decision': {'icon': '💠', 'color': '#ffc107'},
            'system': {'icon': '🖥️', 'color': '#17a2b8'},
            'end': {'icon': '🔴', 'color': '#dc3545'}
        }
        
        for step in suggestions.get('steps', []):
            step_type = step.get('type', 'action')
            style = type_styles.get(step_type, {'icon': '▶️', 'color': '#6c757d'})
            
            st.markdown(f"""
            <div class="step-card">
                <div>
                    <strong>{style['icon']} {step['name']}</strong>
                    <span class="step-type" style="background-color: {style['color']};">
                        {step_type.upper()}
                    </span>
                    <span class="step-time">⏱️ {step.get('expected_time', 'N/A')}</span>
                </div>
                <div class="step-description">
                    📝 {step.get('description', 'Sem descrição')}
                    {f'<br>🔧 Sistema: {step["system"]}' if step.get('system') else '<div>'}
                </div>
                {f'''
                <div class="step-dependencies">
                    📎 Depende de: {', '.join(step.get('dependencies', []))}
                </div>
                ''' if step.get('dependencies') else ''}
            </div>
            """, unsafe_allow_html=True)
        
        # Conexões do Processo
        if suggestions.get('connections'):
            st.write("### 🔗 Conexões")
            for conn in suggestions['connections']:
                st.markdown(f"""
                <div class="step-card">
                    <div>
                        <strong>{conn['source']} ➡️ {conn['target']}</strong>
                        <span class="step-type" style="background-color: #6610f2; color: white;">
                            {conn['type'].upper()}
                        </span>
                    </div>
                    <div class="step-description">
                        🏷️ {conn.get('label', 'Sem rótulo')}
                        {f'<br>❓ Condição: {conn["condition"]}<br>' if conn.get('condition') else '<br>'}
                        📝 {conn.get('reasoning', '') or 'Sem justificativa'}
                </div>
                """, unsafe_allow_html=True)
        
        # Sistemas e Ferramentas
        st.write("### 🔧 Sistemas e Ferramentas")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sistemas Envolvidos:**")
            for system in suggestions.get('process_analysis', {}).get('systems_involved', []):
                st.info(f"""
                🖥️ **{system['name']}**
                - Etapas: {', '.join(system['steps'])}
                - Propósito: {system['purpose']}
                """)
        
        with col2:
            st.write("**Ferramentas:**")
            for tool in suggestions.get('details', {}).get('tools', []):
                st.write(f"• {tool}")
        
        # Dados do Processo
        st.write("### 📊 Dados do Processo")
        details = suggestions.get('details', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Tipos de Dados:**")
            for dtype in details.get('data_types', []):
                st.write(f"• {dtype}")
                
            st.write("**Formatos de Dados:**")
            for fmt in details.get('data_formats', []):
                st.write(f"• {fmt}")
        
        with col2:
            st.write("**Fontes de Dados:**")
            for src in details.get('data_sources', []):
                st.write(f"• {src}")
                
            st.write("**Volume de Dados:**")
            st.write(f"• {details.get('data_volume', 'Não especificado')}")
        
        # Regras e Exceções
        st.write("### 📋 Regras e Exceções")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Regras de Negócio:**")
            for rule in suggestions.get('business_rules', {}).get('business_rules', []):
                st.write(f"• {rule}")
        
        with col2:
            st.write("**Exceções:**")
            for exc in suggestions.get('business_rules', {}).get('exceptions', []):
                st.write(f"• {exc}")
        
        # Objetivos e KPIs
        st.write("### 🎯 Objetivos e KPIs")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Objetivos:**")
            for goal in suggestions.get('automation_goals', {}).get('automation_goals', []):
                st.write(f"• {goal}")
        
        with col2:
            st.write("**KPIs:**")
            for kpi in suggestions.get('automation_goals', {}).get('kpis', []):
                st.write(f"• {kpi}")
    
    with tab2:
        st.json(suggestions)

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
        
        if validate_and_submit(data, ["process_name", "process_owner"], on_submit):
            try:
                # Analisa a descrição com IA
                ai_service = AIService()
                suggestions = ai_service.analyze_process_description(description)
                st.session_state.ai_suggestions = suggestions
                st.session_state.suggestions_processed = False  # Reset flag
                
                # Mostra opções para aplicar sugestões
                st.success("Descrição analisada com sucesso!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Aplicar Sugestões", use_container_width=True):
                        st.session_state.current_step = "details"  # Avança para próxima página
                        st.rerun()
                with col2:
                    if st.button("❌ Ignorar Sugestões", use_container_width=True):
                        st.session_state.ai_suggestions = {}
                        st.info("Sugestões ignoradas. Continue o preenchimento normalmente.")
                
            except Exception as e:
                st.error(f"Erro ao analisar descrição: {str(e)}")
            
            st.success("Informações salvas com sucesso!")

    # Mostra sugestões da IA fora do formulário, apenas se existirem
    if 'ai_suggestions' in st.session_state and st.session_state.ai_suggestions:
        st.write("---")
        st.subheader("🤖 Análise da IA")
        st.info("A IA analisou sua descrição e identificou as seguintes informações:")
        render_ai_suggestions_debug(st.session_state.ai_suggestions)

def filter_valid_options(suggested_values: List[str], valid_options: List[str]) -> List[str]:
    """Filtra valores sugeridos para incluir apenas opções válidas."""
    return [value for value in suggested_values if value in valid_options]

def validate_step_field(step: dict, field: str, value: any) -> tuple[bool, str]:
    """Valida um campo específico de uma etapa em tempo real."""
    if field == 'name':
        if not value.strip():
            return False, "Nome da etapa é obrigatório"
        if len(value) > 100:
            return False, "Nome deve ter no máximo 100 caracteres"
        return True, ""
        
    elif field == 'type':
        valid_types = ["action", "decision", "system", "start", "end"]
        if value not in valid_types:
            return False, "Tipo de etapa inválido"
        return True, ""
        
    elif field == 'description':
        if len(value) > 500:
            return False, "Descrição deve ter no máximo 500 caracteres"
        return True, ""
        
    elif field == 'sla':
        if value:
            sla = value.lower()
            if not any(unit in sla for unit in ['minuto', 'hora', 'dia', 'semana', 'mes', 'mês']):
                return False, "Inclua uma unidade de tempo válida (ex: minutos, horas)"
        return True, ""
        
    elif field == 'dependencies':
        if step['id'] in value:
            return False, "Uma etapa não pode depender dela mesma"
            
        valid_ids = {s['id'] for s in st.session_state.process_steps}
        invalid_deps = [dep for dep in value if dep not in valid_ids]
        if invalid_deps:
            return False, f"Dependências inválidas: {', '.join(invalid_deps)}"
        return True, ""
    
    return True, ""

def render_step_card(step: dict, on_edit: callable, on_delete: callable):
    """Renderiza um card para uma etapa do processo."""
    st.markdown("""
    <style>
    .step-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        background-color: #f8f9fa;
    }
    .step-type {
        font-size: 0.8em;
        padding: 2px 8px;
        border-radius: 12px;
        margin-left: 8px;
        color: white;
    }
    .step-time {
        float: right;
        color: #666;
        font-size: 0.8em;
    }
    .step-description {
        color: #666;
        font-size: 0.9em;
        margin-top: 5px;
    }
    .step-dependencies {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
        border-top: 1px solid #eee;
        padding-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Mapeamento de tipos para ícones e cores
    type_styles = {
        'start': {'icon': '🟢', 'color': '#28a745'},
        'action': {'icon': '▶️', 'color': '#007bff'},
        'decision': {'icon': '💠', 'color': '#ffc107'},
        'system': {'icon': '🖥️', 'color': '#17a2b8'},
        'end': {'icon': '🔴', 'color': '#dc3545'}
    }

    step_type = step.get('type', 'action')
    style = type_styles.get(step_type, {'icon': '▶️', 'color': '#6c757d'})

    st.markdown(f"""
    <div class="step-card">
        <div>
            <strong>{style['icon']} {step['name']}</strong>
            <span class="step-type" style="background-color: {style['color']};">
                {step_type.upper()}
            </span>
            <span class="step-time">⏱️ {step.get('expected_time', 'N/A')}</span>
        </div>
        <div class="step-description">
            📝 {step.get('description', 'Sem descrição')}
            {f'<br>🔧 Sistema: {step["system"]}' if step.get('system') else '<div>'}
        </div>
        {f'''
        <div class="step-dependencies">
            📎 Depende de: {', '.join(step.get('dependencies', []))}
        </div>
        ''' if step.get('dependencies') else ''}
    </div>
    """, unsafe_allow_html=True)

    # Botões de ação
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️", key=f"delete_{step['id']}", help="Remover esta etapa"):
            on_delete(step['id'])

    # Painel de edição expandível
    with st.expander("✏️ Editar", expanded=False):
        # Nome da etapa
        new_name = st.text_input(
            "Nome da Etapa *",
            value=step['name'],
            key=f"edit_name_{step['id']}",
            help="Nome descritivo da etapa (máx. 100 caracteres)"
        )

        # Tipo da etapa
        type_options = {
            'Ação': 'action',
            'Decisão': 'decision',
            'Sistema': 'system',
            'Início': 'start',
            'Fim': 'end'
        }
        current_type = next(
            (pt for pt, en in type_options.items() if en == step['type']),
            'Ação'
        )
        new_type = st.selectbox(
            "Tipo *",
            options=list(type_options.keys()),
            index=list(type_options.keys()).index(current_type),
            key=f"edit_type_{step['id']}",
            help="Tipo de operação realizada nesta etapa"
        )

        # Descrição
        new_description = st.text_area(
            "Descrição",
            value=step.get('description', ''),
            key=f"edit_desc_{step['id']}",
            help="Descrição detalhada da etapa",
            max_chars=500
        )

        # Sistema (se aplicável)
        if type_options[new_type] == 'system':
            new_system = st.text_input(
                "Sistema",
                value=step.get('system', ''),
                key=f"edit_system_{step['id']}",
                help="Nome do sistema utilizado"
            )
        else:
            new_system = None

        # Tempo estimado
        new_time = st.text_input(
            "Tempo Estimado",
            value=step.get('expected_time', ''),
            key=f"edit_time_{step['id']}",
            help="Ex: 5 minutos, 1 hora"
        )

        # Botão de salvar
        if st.button("💾 Salvar Alterações", key=f"save_{step['id']}"):
            step.update({
                'name': new_name,
                'type': type_options[new_type],
                'description': new_description,
                'expected_time': new_time,
                'updated_at': datetime.now().isoformat()
            })
            if new_system is not None:
                step['system'] = new_system
            st.success("Alterações salvas!")
            st.rerun()

def render_tool_card(i: int, tool: dict, on_delete: Callable):
    """Renderiza um card para uma ferramenta/sistema customizado."""
    with st.container():
        st.markdown(f'<div class="step-card">', unsafe_allow_html=True)
        
        # Cabeçalho com número e botões
        col1, col2, col3 = st.columns([8, 1, 1])
        with col1:
            st.subheader(f"Sistema {i+1}")
        with col2:
            if st.button("⬆️", key=f"tool_up_{i}", help="Mover para cima"):
                if i > 0:
                    st.session_state.custom_tools[i], st.session_state.custom_tools[i-1] = \
                        st.session_state.custom_tools[i-1], st.session_state.custom_tools[i]
                    st.rerun()
        with col3:
            if st.button("🗑️", key=f"tool_del_{i}", help="Remover sistema"):
                on_delete(i)
        
        # Nome do sistema
        tool['name'] = st.text_input(
            "Nome do Sistema",
            value=tool.get('name', ''),
            key=f"tool_name_{i}",
            placeholder="Ex: Sistema Interno XYZ"
        )
        
        # Descrição do sistema (opcional)
        tool['description'] = st.text_area(
            "Descrição do Sistema (opcional)",
            value=tool.get('description', ''),
            key=f"tool_desc_{i}",
            placeholder="Descreva o sistema e seu papel no processo...",
            help="Forneça informações adicionais sobre este sistema"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_process_details(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de detalhes do processo."""
    # Inicialização do estado
    if 'process_steps' not in st.session_state:
        st.session_state.process_steps = []
    
    if 'editing_step' not in st.session_state:
        st.session_state.editing_step = None
    
    if 'custom_tools' not in st.session_state:
        st.session_state.custom_tools = []
    
    # Se temos sugestões da IA e o formulário ainda não foi processado
    if 'ai_suggestions' in st.session_state and not st.session_state.get('suggestions_processed'):
        suggestions = st.session_state.ai_suggestions
        
        # Usa diretamente os steps da IA
        st.session_state.process_steps = suggestions.get('steps', [])
        
        # Atualiza os sistemas identificados
        systems = suggestions.get('process_analysis', {}).get('systems_involved', [])
        st.session_state.custom_tools = [system['name'] for system in systems]
        
        # Atualiza os dados do processo com valores da IA
        details = suggestions.get('details', {})
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {}
            
        st.session_state.form_data['details'] = {
            'steps': details.get('steps', []),
            'tools': {
                'common_tools': [],
                'custom_tools': st.session_state.custom_tools
            },
            'data_types': details.get('data_types', []),
            'data_formats': details.get('data_formats', []),
            'data_sources': details.get('data_sources', []),
            'data_volume': details.get('data_volume', 'Médio')
        }
        
        # Marca que as sugestões foram processadas
        st.session_state.suggestions_processed = True
        st.rerun()
    
    # Interface do usuário
    st.write("### 📝 Detalhes do Processo")
    
    # Tabs principais para organizar o conteúdo
    tab_steps, tab_diagram, tab_editor, tab_systems, tab_data = st.tabs([
        "📋 Etapas",
        "📊 Diagrama",
        "✏️ Editor",
        "🔧 Sistemas",
        "📊 Dados"
    ])
    
    with tab_steps:
        # Lista de etapas existentes
        for step in st.session_state.process_steps:
            render_step_card(
                step,
                on_edit=lambda id: None,
                on_delete=lambda id: st.session_state.process_steps.remove(
                    next(s for s in st.session_state.process_steps if s['id'] == id)
                )
            )
        
        # Botão para adicionar nova etapa
        if st.button("➕ Nova Etapa", use_container_width=True):
            new_id = f"node_{len(st.session_state.process_steps)}"
            st.session_state.process_steps.append({
                'id': new_id,
                'name': '',
                'description': '',
                'type': 'action',
                'system': '',
                'expected_time': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            st.rerun()
    
    with tab_systems:
        # Sistemas identificados pela IA
        if 'ai_suggestions' in st.session_state:
            systems = st.session_state.ai_suggestions.get('process_analysis', {}).get('systems_involved', [])
            if systems:
                st.write("**🤖 Sistemas Identificados pela IA:**")
                for system in systems:
                    with st.expander(f"🖥️ {system['name']}", expanded=True):
                        st.write(f"**Propósito:** {system['purpose']}")
                        st.write("**Etapas envolvidas:**")
                        for step_id in system['steps']:
                            step = next((s for s in st.session_state.process_steps if s['id'] == step_id), None)
                            if step:
                                st.info(f"• {step['name']}")
        
        st.divider()
        
        # Interface para sistemas comuns e customizados
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sistemas Comuns**")
            common_tools = st.multiselect(
                "Selecione os sistemas utilizados:",
                OPTIONS['common_tools'],
                default=st.session_state.get('common_tools', []),
                help="Sistemas e ferramentas comumente usados"
            )
        
        with col2:
            st.write("**Sistemas Customizados**")
            new_tool = st.text_input(
                "Adicionar novo sistema:",
                key="new_tool_input",
                placeholder="Ex: SAP, Portal Interno, etc."
            )
            if st.button("➕ Adicionar Sistema"):
                if new_tool and new_tool not in st.session_state.custom_tools:
                    st.session_state.custom_tools.append(new_tool)
                    st.rerun()
            
            for idx, tool in enumerate(st.session_state.custom_tools):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.info(f"• {tool}")
                with col_b:
                    if st.button("🗑️", key=f"del_tool_{idx}"):
                        st.session_state.custom_tools.pop(idx)
                        st.rerun()
    
    with tab_data:
        details = st.session_state.ai_suggestions.get('details', {}) if 'ai_suggestions' in st.session_state else {}
        
        # Processa os dados sugeridos pela IA
        suggested_data_types = details.get('data_types', [])
        suggested_data_formats = details.get('data_formats', [])
        suggested_data_sources = details.get('data_sources', [])
        
        # Adiciona sugestões da IA às opções disponíveis
        all_data_types = list(set(OPTIONS['data_types'] + suggested_data_types))
        all_data_formats = list(set(OPTIONS['data_formats'] + suggested_data_formats))
        all_data_sources = list(set(OPTIONS['data_sources'] + suggested_data_sources))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Tipos e Formatos**")
            
            # Mostra sugestões da IA
            if suggested_data_types:
                st.info("🤖 Sugestões da IA:")
                for dtype in suggested_data_types:
                    st.write(f"• {dtype}")
                st.divider()
            
            data_types = st.multiselect(
                "Tipos de Dados:",
                options=all_data_types,
                default=suggested_data_types,
                help="Tipos de dados manipulados no processo"
            )
            
            # Mostra sugestões da IA
            if suggested_data_formats:
                st.info("🤖 Sugestões da IA:")
                for fmt in suggested_data_formats:
                    st.write(f"• {fmt}")
                st.divider()
            
            data_formats = st.multiselect(
                "Formatos de Dados:",
                options=all_data_formats,
                default=suggested_data_formats,
                help="Formatos de arquivos e dados utilizados"
            )
        
        with col2:
            st.write("**Fontes e Volume**")
            
            # Mostra sugestões da IA
            if suggested_data_sources:
                st.info("🤖 Sugestões da IA:")
                for src in suggested_data_sources:
                    st.write(f"• {src}")
                st.divider()
            
            data_sources = st.multiselect(
                "Fontes de Dados:",
                options=all_data_sources,
                default=suggested_data_sources,
                help="De onde os dados são obtidos"
            )
            
            data_volume = st.select_slider(
                "Volume de Dados:",
                options=["Baixo", "Médio", "Alto"],
                value=details.get('data_volume', "Médio"),
                help="Volume diário de dados processados"
            )
    
    # Botão de salvar
    st.divider()
    if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
        data = {
            "steps": st.session_state.process_steps,
            "tools": {
                "common_tools": common_tools,
                "custom_tools": st.session_state.custom_tools
            },
            "data_types": data_types,
            "data_formats": data_formats,
            "data_sources": data_sources,
            "data_volume": data_volume
        }
        
        if validate_and_submit(data, ["steps"], on_submit):
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
        
        # Atualiza o estado com as sugestões (mantendo como listas)
        if 'business_rules' not in st.session_state:
            st.session_state.business_rules = {
                'selected_rules': standard_rules,
                'custom_rules': custom_rules,  # Mantém como lista
                'selected_exceptions': standard_exceptions,
                'custom_exceptions': custom_exceptions  # Mantém como lista
            }
        else:
            st.session_state.business_rules.update({
                'selected_rules': standard_rules,
                'custom_rules': custom_rules,  # Mantém como lista
                'selected_exceptions': standard_exceptions,
                'custom_exceptions': custom_exceptions  # Mantém como lista
            })
    
    # Debug para verificar os dados processados
    st.write("Debug - Dados Processados:", {
        'saved_data': saved_data,
        'business_rules_state': st.session_state.business_rules
    })
    
    # Interface para adicionar/remover regras customizadas
    st.write("### Regras de Negócio")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Regras Customizadas Atuais:**")
        custom_rules = st.session_state.business_rules.get('custom_rules', [])
        for idx, rule in enumerate(custom_rules):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.info(f"• {rule}")
            with col_b:
                if st.button("🗑️", key=f"del_rule_{idx}"):
                    custom_rules.remove(rule)
                    st.rerun()
    
    with col2:
        st.write("**Adicionar Nova Regra**")
        new_rule = st.text_input("", 
                                placeholder="Digite uma nova regra",
                                key="new_rule_input")
        if st.button("➕ Adicionar", key="add_rule_btn"):
            if new_rule and new_rule not in custom_rules:
                custom_rules.append(new_rule)
                st.rerun()
    
    # Interface para adicionar/remover exceções customizadas
    st.write("### Exceções e Tratamentos")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Exceções Customizadas Atuais:**")
        custom_exceptions = st.session_state.business_rules.get('custom_exceptions', [])
        for idx, exception in enumerate(custom_exceptions):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.info(f"• {exception}")
            with col_b:
                if st.button("🗑️", key=f"del_exception_{idx}"):
                    custom_exceptions.remove(exception)
                    st.rerun()
    
    with col2:
        st.write("**Adicionar Nova Exceção**")
        new_exception = st.text_input("", 
                                    placeholder="Digite uma nova exceção",
                                    key="new_exception_input")
        if st.button("➕ Adicionar", key="add_exception_btn"):
            if new_exception and new_exception not in custom_exceptions:
                custom_exceptions.append(new_exception)
                st.rerun()
    
    # Formulário principal para seleção e salvamento
    with st.form("rules_form", clear_on_submit=False):
        # Templates de regras comuns
        selected_rules = st.multiselect(
            "Regras comuns:",
            OPTIONS.get('business_rules_templates', []),
            default=st.session_state.business_rules.get('selected_rules', []),
            help="Selecione as regras aplicáveis ao processo"
        )
        
        # Exceções comuns
        selected_exceptions = st.multiselect(
            "Exceções comuns:",
            OPTIONS.get('common_exceptions', []),
            default=st.session_state.business_rules.get('selected_exceptions', []),
            help="Selecione as exceções aplicáveis ao processo"
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
            data = {
                "business_rules": selected_rules + custom_rules,
                "exceptions": selected_exceptions + custom_exceptions
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
        
        # Atualiza o estado com as sugestões (mantendo como listas)
        if 'automation_goals' not in st.session_state:
            st.session_state.automation_goals = {
                'selected_goals': standard_goals,
                'custom_goals': custom_goals,  # Mantém como lista
                'selected_kpis': standard_kpis,
                'custom_kpis': custom_kpis  # Mantém como lista
            }
        else:
            st.session_state.automation_goals.update({
                'selected_goals': standard_goals,
                'custom_goals': custom_goals,  # Mantém como lista
                'selected_kpis': standard_kpis,
                'custom_kpis': custom_kpis  # Mantém como lista
            })
    
    # Debug para verificar os dados processados
    st.write("Debug - Dados Processados:", {
        'saved_data': saved_data,
        'automation_goals_state': st.session_state.get('automation_goals', {})
    })
    
    # Interface para adicionar/remover objetivos customizados
    st.write("### Objetivos da Automação")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Objetivos Customizados Atuais:**")
        custom_goals = st.session_state.get('automation_goals', {}).get('custom_goals', [])
        for idx, goal in enumerate(custom_goals):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.info(f"• {goal}")
            with col_b:
                if st.button("🗑️", key=f"del_goal_{idx}"):
                    custom_goals.remove(goal)
                    st.rerun()
    
    with col2:
        st.write("**Adicionar Novo Objetivo**")
        new_goal = st.text_input("", 
                                placeholder="Digite um novo objetivo",
                                key="new_goal_input")
        if st.button("➕ Adicionar", key="add_goal_btn"):
            if new_goal and new_goal not in custom_goals:
                custom_goals.append(new_goal)
                st.rerun()
    
    # Interface para adicionar/remover KPIs customizados
    st.write("### KPIs e Métricas")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**KPIs Customizados Atuais:**")
        custom_kpis = st.session_state.get('automation_goals', {}).get('custom_kpis', [])
        for idx, kpi in enumerate(custom_kpis):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.info(f"• {kpi}")
            with col_b:
                if st.button("🗑️", key=f"del_kpi_{idx}"):
                    custom_kpis.remove(kpi)
                    st.rerun()
    
    with col2:
        st.write("**Adicionar Novo KPI**")
        new_kpi = st.text_input("", 
                               placeholder="Digite um novo KPI",
                               key="new_kpi_input")
        if st.button("➕ Adicionar", key="add_kpi_btn"):
            if new_kpi and new_kpi not in custom_kpis:
                custom_kpis.append(new_kpi)
                st.rerun()
    
    # Formulário principal para seleção e salvamento
    with st.form("goals_form", clear_on_submit=False):
        # Seleção de objetivos comuns
        selected_goals = st.multiselect(
            "Objetivos comuns:",
            OPTIONS['automation_goals'],
            default=st.session_state.get('automation_goals', {}).get('selected_goals', []),
            help="Selecione os objetivos aplicáveis ao processo"
        )
        
        # Seleção de KPIs comuns
        selected_kpis = st.multiselect(
            "KPIs comuns:",
            OPTIONS['kpi_templates'],
            default=st.session_state.get('automation_goals', {}).get('selected_kpis', []),
            help="Selecione os KPIs aplicáveis ao processo"
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
            data = {
                "automation_goals": selected_goals + custom_goals,
                "kpis": selected_kpis + custom_kpis
            }
            
            if validate_and_submit(data, ["automation_goals", "kpis"], on_submit):
                st.success("Objetivos e KPIs salvos com sucesso!")

def validate_step(step: dict) -> tuple[bool, list[str]]:
    """Valida os dados de uma etapa do processo."""
    errors = []
    
    # Validação do nome
    if not step.get('name', '').strip():
        errors.append("Nome da etapa é obrigatório")
    elif len(step['name']) > 100:
        errors.append("Nome da etapa deve ter no máximo 100 caracteres")
    
    # Validação do tipo
    valid_types = ["action", "decision", "system", "start", "end"]
    if step.get('type') not in valid_types:
        errors.append("Tipo de etapa inválido")
    
    # Validação da descrição
    if step.get('description') and len(step['description']) > 500:
        errors.append("Descrição deve ter no máximo 500 caracteres")
    
    # Validação do SLA
    if step.get('sla'):
        sla = step['sla'].lower()
        if not any(unit in sla for unit in ['minuto', 'hora', 'dia', 'semana', 'mes', 'mês']):
            errors.append("SLA deve incluir uma unidade de tempo válida")
    
    # Validação de dependências
    if step.get('dependencies'):
        # Verifica se não há dependência circular
        if step['id'] in step['dependencies']:
            errors.append("Uma etapa não pode depender dela mesma")
        
        # Verifica se todas as dependências existem
        valid_ids = {s['id'] for s in st.session_state.process_steps}
        invalid_deps = [dep for dep in step['dependencies'] if dep not in valid_ids]
        if invalid_deps:
            errors.append(f"Dependências inválidas: {', '.join(invalid_deps)}")
    
    return len(errors) == 0, errors

def render_debug_section():
    """Renderiza uma seção de debug com os dados do processo."""
    st.write("### 🔍 Debug Detalhado")
    
    # Usa tabs para organizar os dados
    tabs = st.tabs([
        "📋 Etapas", 
        "🔧 Sistemas", 
        "📊 Estado", 
        "📝 Dados Iniciais", 
        "🤖 Sugestões IA",
        "📄 Form Data"
    ])
    
    with tabs[0]:
        st.write("#### Etapas do Processo")
        st.write(f"Total de etapas: {len(st.session_state.process_steps)}")
        
        # Usa uma tabela para mostrar as etapas
        steps_data = []
        for i, step in enumerate(st.session_state.process_steps, 1):
            steps_data.append({
                "Nº": i,
                "ID": step['id'],
                "Nome": step['name'],
                "Tipo": step['type'],
                "Descrição": step.get('description', ''),
                "Dependências": ', '.join(step.get('dependencies', [])),
                "Criado em": step['created_at'],
                "Atualizado em": step['updated_at']
            })
        
        # Mostra os dados em formato de tabela
        if steps_data:
            st.dataframe(
                steps_data,
                use_container_width=True,
                column_config={
                    "Nº": st.column_config.NumberColumn(width=50),
                    "ID": st.column_config.TextColumn(width=100),
                    "Nome": st.column_config.TextColumn(width=200),
                    "Tipo": st.column_config.TextColumn(width=100),
                    "Descrição": st.column_config.TextColumn(width=200),
                    "Dependências": st.column_config.TextColumn(width=150),
                    "Criado em": st.column_config.DatetimeColumn(width=150),
                    "Atualizado em": st.column_config.DatetimeColumn(width=150)
                }
            )
        
        # Dados brutos em JSON
        st.write("**Dados Brutos:**")
        st.json(st.session_state.process_steps)
    
    with tabs[1]:
        st.write("#### Sistemas")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sistemas Comuns:**")
            st.json(st.session_state.get('common_tools', []))
        
        with col2:
            st.write("**Sistemas Customizados:**")
            st.json(st.session_state.custom_tools)
    
    with tabs[2]:
        st.write("#### Estado da Sessão")
        state_data = {
            'editing_step': st.session_state.editing_step,
            'debug_mode': st.session_state.get('debug_mode', False),
            'current_step': st.session_state.get('current_step'),
            'form_submitted': st.session_state.get('form_submitted', False)
        }
        st.json(state_data)
    
    with tabs[3]:
        st.write("#### Dados Iniciais")
        st.json(st.session_state.get('initial_data', {}))
    
    with tabs[4]:
        st.write("#### Sugestões da IA")
        if 'ai_suggestions' in st.session_state:
            for key, value in st.session_state.ai_suggestions.items():
                st.write(f"**{key}:**")
                st.json(value)
        else:
            st.info("Nenhuma sugestão da IA disponível")
    
    with tabs[5]:
        st.write("#### Dados do Formulário")
        st.json(st.session_state.form_data)

def infer_step_type(step_name: str) -> str:
    """Infere o tipo da etapa baseado em seu nome/descrição."""
    step_lower = step_name.lower()
    
    # Padrões para identificar tipos de etapas
    if any(word in step_lower for word in ['verificar', 'validar', 'conferir', 'checar']):
        return 'decision'
    elif any(word in step_lower for word in ['sistema', 'acessar', 'login', 'portal', 'sap', 'excel']):
        return 'system'
    elif 'inicio' in step_lower or 'receb' in step_lower or step_lower.startswith('iniciar'):
        return 'start'
    elif 'fim' in step_lower or 'finalizar' in step_lower or 'concluir' in step_lower:
        return 'end'
    else:
        return 'action'

def handle_description_analysis(description: str):
    """Processa a análise da descrição do processo."""
    ai_service = AIService()
    
    try:
        # Analisa a descrição
        analysis = ai_service.analyze_process_description(description)
        
        if analysis and analysis.get('steps'):
            # Atualiza os steps com a nova estrutura
            st.session_state.process_steps = analysis['steps']
            
            # Salva as sugestões de conexões
            st.session_state.ai_suggestions = {
                'connections': analysis.get('connections', []),
                'process_analysis': analysis.get('process_analysis', {})
            }
            
            # Atualiza o diagrama
            editor = DiagramEditor()
            editor._sync_with_process_steps()
            
            st.success("✨ Análise concluída! O diagrama foi atualizado com as conexões sugeridas.")
            
            # Mostra análise do processo
            if 'process_analysis' in analysis:
                with st.expander("📊 Análise do Processo", expanded=True):
                    # Mostra nós iniciais e finais
                    st.write("**🎯 Pontos de Controle:**")
                    st.write(f"• Início: {analysis['process_analysis']['start_node']}")
                    st.write(f"• Fins: {', '.join(analysis['process_analysis']['end_nodes'])}")
                    
                    # Mostra caminhos condicionais
                    if 'conditional_paths' in analysis['process_analysis']:
                        st.write("\n**🔄 Caminhos Condicionais:**")
                        for path in analysis['process_analysis']['conditional_paths']:
                            st.write(f"\n🔹 Decisão: {path['decision_node']}")
                            for condition in path['conditions']:
                                st.write(f"  ↳ Se {condition['condition']} → {condition['target']}")
        else:
            st.error("Não foi possível analisar a descrição. Nenhuma etapa identificada.")
            
    except Exception as e:
        logger.error(f"Erro ao analisar descrição: {str(e)}")
        st.error(f"Erro ao analisar descrição: {str(e)}")