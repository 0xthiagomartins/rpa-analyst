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
    # Estilo para melhor visualização
    st.markdown("""
    <style>
    .debug-section {
        padding: 10px;
        border-left: 3px solid #3498db;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .json-view {
        font-family: monospace;
        white-space: pre;
        padding: 10px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs para organizar a visualização
    tab1, tab2 = st.tabs(["📊 Visualização Formatada", "🔍 JSON Completo"])
    
    with tab1:
        # Etapas do Processo
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**📝 Etapas do Processo:**")
        for step in suggestions.get('steps_as_is', []):
            st.write(f"• {step}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sistemas e Ferramentas
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**🔧 Sistemas e Ferramentas:**")
        for tool in suggestions.get('details', {}).get('tools', []):
            st.write(f"• {tool}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Dados do Processo
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**📊 Dados do Processo:**")
        details = suggestions.get('details', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("*Tipos de Dados:*")
            for dtype in details.get('data_types', []):
                st.write(f"• {dtype}")
                
            st.write("*Formatos de Dados:*")
            for fmt in details.get('data_formats', []):
                st.write(f"• {fmt}")
        
        with col2:
            st.write("*Fontes de Dados:*")
            for src in details.get('data_sources', []):
                st.write(f"• {src}")
                
            st.write("*Volume de Dados:*")
            st.write(f"• {details.get('data_volume', 'Não especificado')}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Regras de Negócio
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**📋 Regras de Negócio:**")
        for rule in suggestions.get('business_rules', {}).get('business_rules', []):
            st.write(f"• {rule}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Exceções
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**⚠️ Exceções:**")
        for exc in suggestions.get('business_rules', {}).get('exceptions', []):
            st.write(f"• {exc}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Objetivos e KPIs
        st.markdown("<div class='debug-section'>", unsafe_allow_html=True)
        st.write("**🎯 Objetivos e KPIs:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write("*Objetivos:*")
            for goal in suggestions.get('automation_goals', {}).get('automation_goals', []):
                st.write(f"• {goal}")
        with col2:
            st.write("*KPIs:*")
            for kpi in suggestions.get('automation_goals', {}).get('kpis', []):
                st.write(f"• {kpi}")
        st.markdown("</div>", unsafe_allow_html=True)
    
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
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .step-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .step-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    .step-type-badge {
        font-size: 0.85em;
        padding: 4px 10px;
        border-radius: 15px;
        margin-left: 10px;
        background: #f0f2f6;
        color: #444;
    }
    .step-content {
        padding: 10px 0;
    }
    .step-description {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
    }
    .image-preview {
        max-height: 200px;
        object-fit: contain;
        margin: 10px auto;
        display: block;
    }
    .image-container {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f'<div class="step-card">', unsafe_allow_html=True)
        
        # Cabeçalho com Nome e Tipo
        cols = st.columns([8, 3, 1])
        
        with cols[0]:
            name = st.text_input(
                "Nome da Etapa *",
                value=step['name'],
                key=f"step_name_{step['id']}",
                help="Nome descritivo da etapa (máx. 100 caracteres)",
                placeholder="Ex: Verificar documentação"
            )
        
        with cols[1]:
            type_mapping = {
                'Ação': ('action', '⚡', '#FF9D00'),
                'Decisão': ('decision', '🔄', '#00B8D4'),
                'Sistema': ('system', '💻', '#7C4DFF'),
                'Início': ('start', '🟢', '#00C853'),
                'Fim': ('end', '🔴', '#FF1744')
            }
            
            current_type_pt = next(
                (pt for pt, (en, _, _) in type_mapping.items() if en == step['type']),
                'Ação'
            )
            
            new_type_pt = st.selectbox(
                "Tipo *",
                list(type_mapping.keys()),
                index=list(type_mapping.keys()).index(current_type_pt),
                key=f"step_type_{step['id']}",
                format_func=lambda x: f"{type_mapping[x][1]} {x}",
                help="Tipo de operação realizada nesta etapa"
            )
        
        with cols[2]:
            if st.button("🗑️", key=f"delete_{step['id']}", help="Remover esta etapa"):
                on_delete(step['id'])
        
        # Validação e atualização dos dados
        is_valid_name, name_error = validate_step_field(step, 'name', name)
        new_type = type_mapping[new_type_pt][0]
        is_valid_type, type_error = validate_step_field(step, 'type', new_type)
        
        if not is_valid_name:
            st.error(name_error)
        elif not is_valid_type:
            st.error(type_error)
        else:
            step['name'] = name
            step['type'] = new_type
            step['updated_at'] = datetime.now().isoformat()
        
        # Descrição e Imagem lado a lado
        with st.expander("📝 Detalhes da Etapa", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                description = st.text_area(
                    "Descrição Detalhada",
                    value=step.get('description', ''),
                    key=f"step_desc_{step['id']}",
                    placeholder="Ex: Nesta etapa, o sistema deve verificar...",
                    help="Máximo de 500 caracteres",
                    max_chars=500,
                    height=150
                )
                
                if description != step.get('description', ''):
                    step['description'] = description
                    step['updated_at'] = datetime.now().isoformat()
            
            with col2:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    "Imagem da Etapa",
                    type=['png', 'jpg', 'jpeg'],
                    key=f"step_img_{step['id']}",
                    help="Faça upload de uma imagem ilustrativa"
                )
                
                # Preview da imagem
                if uploaded_file:
                    st.image(
                        uploaded_file, 
                        caption="Preview",
                        use_container_width=True,
                        output_format="PNG"
                    )
                    step['image'] = uploaded_file.getvalue()
                    step['updated_at'] = datetime.now().isoformat()
                elif step.get('image'):
                    st.image(
                        step['image'], 
                        caption="Imagem atual",
                        use_container_width=True,
                        output_format="PNG"
                    )
                else:
                    st.info("Nenhuma imagem adicionada")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Contador de caracteres
            if description:
                st.caption(f"{len(description)}/500 caracteres")
        
        # Rodapé com informações adicionais
        if step.get('dependencies'):
            st.markdown('<div class="step-footer">', unsafe_allow_html=True)
            deps = [
                next((s['name'] for s in st.session_state.process_steps if s['id'] == dep_id), dep_id)
                for dep_id in step['dependencies']
            ]
            st.markdown(f"📎 **Depende de:** {', '.join(deps)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Converte as sugestões em etapas do processo
        st.session_state.process_steps = [
            {
                'id': f"step_{i}",
                'name': step,
                'description': '',
                'type': infer_step_type(step),
                'responsible': '',
                'sla': '',
                'dependencies': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            for i, step in enumerate(suggestions.get('steps_as_is', []))
        ]
        
        # Atualiza os sistemas identificados
        st.session_state.custom_tools = suggestions.get('details', {}).get('tools', [])
        
        # Filtra os valores sugeridos para garantir que sejam válidos
        suggested_data_types = suggestions.get('details', {}).get('data_types', [])
        valid_data_types = [dt for dt in suggested_data_types if dt in OPTIONS['data_types']]
        
        suggested_data_formats = suggestions.get('details', {}).get('data_formats', [])
        valid_data_formats = [df for df in suggested_data_formats if df in OPTIONS['data_formats']]
        
        suggested_data_sources = suggestions.get('details', {}).get('data_sources', [])
        valid_data_sources = [ds for ds in suggested_data_sources if ds in OPTIONS['data_sources']]
        
        # Atualiza os dados do processo com valores válidos
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {}
            
        st.session_state.form_data['details'] = {
            'steps': suggestions.get('details', {}).get('steps', []),
            'tools': {
                'common_tools': [],
                'custom_tools': st.session_state.custom_tools
            },
            'data_types': valid_data_types,
            'data_formats': valid_data_formats,
            'data_sources': valid_data_sources,
            'data_volume': suggestions.get('details', {}).get('data_volume', 'Médio')
        }
        
        # Marca que as sugestões foram processadas
        st.session_state.suggestions_processed = True
        
        # Força atualização da interface
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
            new_id = f"step_{len(st.session_state.process_steps)}"
            st.session_state.process_steps.append({
                'id': new_id,
                'name': '',
                'description': '',
                'type': 'action',
                'responsible': '',
                'sla': '',
                'dependencies': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            st.rerun()
    
    with tab_diagram:
        # Visualização do diagrama
        from .process_diagram import render_process_diagram
        render_process_diagram()
    
    with tab_editor:
        # Editor visual do diagrama
        render_diagram_editor()
    
    with tab_systems:
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
            # Interface para adicionar sistemas customizados
            new_tool = st.text_input(
                "Adicionar novo sistema:",
                key="new_tool_input",
                placeholder="Ex: SAP, Portal Interno, etc."
            )
            if st.button("➕ Adicionar Sistema"):
                if new_tool and new_tool not in st.session_state.custom_tools:
                    st.session_state.custom_tools.append(new_tool)
                    st.rerun()
            
            # Lista de sistemas customizados
            for idx, tool in enumerate(st.session_state.custom_tools):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.info(f"• {tool}")
                with col_b:
                    if st.button("🗑️", key=f"del_tool_{idx}"):
                        st.session_state.custom_tools.pop(idx)
                        st.rerun()
    
    with tab_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tipos e Formatos**")
            data_types = st.multiselect(
                "Tipos de Dados:",
                OPTIONS['data_types'],
                default=initial_data.get('data_types', []),
                help="Tipos de dados manipulados no processo"
            )
            
            data_formats = st.multiselect(
                "Formatos de Dados:",
                OPTIONS['data_formats'],
                default=initial_data.get('data_formats', []),
                help="Formatos de arquivos e dados utilizados"
            )
        
        with col2:
            st.write("**Fontes e Volume**")
            data_sources = st.multiselect(
                "Fontes de Dados:",
                OPTIONS['data_sources'],
                default=initial_data.get('data_sources', []),
                help="De onde os dados são obtidos"
            )
            
            data_volume = st.select_slider(
                "Volume de Dados:",
                options=["Baixo", "Médio", "Alto"],
                value=initial_data.get('data_volume', "Médio"),
                help="Volume diário de dados processados"
            )
    
    # Botão de salvar (fixo na parte inferior)
    st.divider()
    if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
        data = {
            "steps": [step['name'] for step in st.session_state.process_steps],
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
    
    # Debug no final, colapsado por padrão
    with st.expander("🔍 Debug", expanded=False):
        render_debug_section()

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