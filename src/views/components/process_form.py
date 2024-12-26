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
                
                # Mostra opções para aplicar sugestões
                st.success("Descrição analisada com sucesso!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Aplicar Sugestões", use_container_width=True):
                        # Aplica as sugestões aos dados do formulário
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

    # Mostra sugestões da IA fora do formulário, apenas se existirem
    if 'ai_suggestions' in st.session_state and st.session_state.ai_suggestions:
        st.write("---")
        st.subheader("🤖 Análise da IA")
        st.info("A IA analisou sua descrição e identificou as seguintes informações:")
        render_ai_suggestions_debug(st.session_state.ai_suggestions)

def filter_valid_options(suggested_values: List[str], valid_options: List[str]) -> List[str]:
    """Filtra valores sugeridos para incluir apenas opções válidas."""
    return [value for value in suggested_values if value in valid_options]

def render_step_card(i: int, step: dict, on_delete: Callable):
    """Renderiza um card para uma etapa do processo."""
    with st.container():
        st.markdown("""
        <style>
        .step-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 3px solid #1f77b4;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f'<div class="step-card">', unsafe_allow_html=True)
            
            # Cabeçalho com número da etapa e botões
            col1, col2, col3 = st.columns([8, 1, 1])
            with col1:
                st.subheader(f"Etapa {i+1}")
            with col2:
                if st.button("⬆️", key=f"up_{i}", help="Mover para cima"):
                    if i > 0:
                        st.session_state.process_steps[i], st.session_state.process_steps[i-1] = \
                            st.session_state.process_steps[i-1], st.session_state.process_steps[i]
                        st.rerun()
            with col3:
                if st.button("🗑️", key=f"del_{i}", help="Remover etapa"):
                    on_delete(i)
            
            # Nome da etapa
            step['name'] = st.text_input(
                "Nome da Etapa",
                value=step.get('name', ''),
                key=f"step_name_{i}",
                placeholder="Ex: Acessar sistema"
            )
            
            # Descrição detalhada (opcional)
            step['description'] = st.text_area(
                "Descrição Detalhada (opcional)",
                value=step.get('description', ''),
                key=f"step_desc_{i}",
                placeholder="Descreva os detalhes desta etapa...",
                help="Forneça informações adicionais sobre esta etapa"
            )
            
            # Upload de imagem (opcional)
            uploaded_file = st.file_uploader(
                "Imagem da Etapa (opcional)",
                type=['png', 'jpg', 'jpeg'],
                key=f"step_img_{i}",
                help="Faça upload de uma imagem ilustrativa"
            )
            
            if uploaded_file:
                step['image'] = uploaded_file.getvalue()
                st.image(step['image'], caption=f"Imagem da Etapa {i+1}", use_column_width=True)
            elif 'image' in step and step['image']:
                st.image(step['image'], caption=f"Imagem da Etapa {i+1}", use_column_width=True)
            
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

def render_step_edit_modal(step: dict, step_number: int):
    """Renderiza o modal de edição de etapa."""
    modal = Modal(
        "Editar Etapa",
        key=f"modal_edit_step_{step_number}"
    )

    if modal.is_open():
        with modal.container():
            with st.form(f"edit_step_form_{step_number}"):
                st.write(f"### Editar Etapa {step_number + 1}")
                
                # Nome da etapa
                new_name = st.text_input(
                    "Nome da Etapa",
                    value=step.get('name', ''),
                    placeholder="Ex: Acessar sistema"
                )
                
                # Descrição detalhada
                new_description = st.text_area(
                    "Descrição Detalhada",
                    value=step.get('description', ''),
                    placeholder="Descreva os detalhes desta etapa..."
                )
                
                # Upload de imagem
                uploaded_file = st.file_uploader(
                    "Imagem da Etapa",
                    type=['png', 'jpg', 'jpeg']
                )
                
                if uploaded_file:
                    new_image = uploaded_file.getvalue()
                    st.image(new_image, caption="Preview da Imagem")
                elif step.get('image'):
                    st.image(step['image'], caption="Imagem Atual")
                    new_image = step['image']
                else:
                    new_image = None
                
                # Botões de ação
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar"):
                        step.update({
                            'name': new_name,
                            'description': new_description,
                            'image': new_image
                        })
                        modal.close()
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("❌ Cancelar"):
                        modal.close()
                        st.rerun()

def render_process_details(on_submit: Optional[Callable] = None, initial_data: dict = None):
    """Renderiza o formulário de detalhes do processo."""
    # Usa dados salvos ou iniciais
    saved_data = st.session_state.form_data.get('details', {})
    initial_data = saved_data or initial_data or {}
    
    # Verifica se já temos uma descrição do processo
    process_description = st.session_state.form_data.get('identification', {}).get('process_description', '')
    
    # Se temos uma descrição e não temos dados inferidos, vamos inferir
    if process_description and not saved_data:
        try:
            ai_service = AIService()
            analysis = ai_service.analyze_process_description(process_description)
            
            # Filtra as sugestões para incluir apenas opções válidas
            initial_data = {
                'steps': analysis['details'].get('steps', []),
                'tools': {
                    'common_tools': filter_valid_options(
                        analysis['details'].get('tools', []),
                        OPTIONS['systems']['common_tools']
                    ),
                    'custom_tools': []
                },
                'data_types': filter_valid_options(
                    analysis['details'].get('data_types', []),
                    OPTIONS['data_types']
                ),
                'data_formats': filter_valid_options(
                    analysis['details'].get('data_formats', []),
                    OPTIONS['data_formats']
                ),
                'data_sources': filter_valid_options(
                    analysis['details'].get('data_sources', []),
                    OPTIONS['data_sources']
                ),
                'data_volume': analysis['details'].get('data_volume', 'Médio')
            }
        except Exception as e:
            st.warning(f"Não foi possível inferir dados automaticamente: {str(e)}")
    
    # Inicializa estruturas de dados mais ricas
    if 'process_steps' not in st.session_state:
        steps = initial_data.get('steps', [])
        st.session_state.process_steps = [{'name': step} for step in steps] if steps else [{'name': ''}]
    
    # Inicializa sistemas customizados
    if 'custom_tools' not in st.session_state:
        tools_data = initial_data.get('tools', {})
        custom_tools = []
        
        # Adiciona ferramentas inferidas pela IA
        if 'ai_suggestions' in st.session_state:
            ai_tools = st.session_state.ai_suggestions.get('details', {}).get('tools', [])
            if ai_tools:
                for tool in ai_tools:
                    # Extrai o nome base do sistema e sua descrição
                    if "(" in tool and ")" in tool:
                        tool_name = tool[:tool.find("(")].strip()
                        tool_desc = tool[tool.find("(")+1:tool.find(")")].strip()
                    else:
                        tool_name = tool.strip()
                        tool_desc = ""
                    
                    # Se não for um sistema comum, adiciona aos customizados
                    if tool_name not in OPTIONS['systems']['common_tools']:
                        custom_tools.append({
                            'name': tool_name,
                            'description': tool_desc
                        })
                    # Se for um sistema comum, adiciona à lista de seleção padrão
                    else:
                        if 'common_tools' not in initial_data.get('tools', {}):
                            initial_data.setdefault('tools', {})['common_tools'] = []
                        if tool_name not in initial_data['tools']['common_tools']:
                            initial_data['tools']['common_tools'].append(tool_name)
        
        # Adiciona ferramentas customizadas dos dados iniciais
        if isinstance(tools_data, dict):
            for tool in tools_data.get('custom_tools', []):
                if not any(t['name'] == tool for t in custom_tools):
                    custom_tools.append({'name': tool})
        
        # Se não houver nenhuma ferramenta, adiciona uma vazia
        st.session_state.custom_tools = custom_tools if custom_tools else [{'name': '', 'description': ''}]
    
    # Controles de estado
    if 'editing_step' not in st.session_state:
        st.session_state.editing_step = None
    
    # Gerenciamento de etapas (fora do form)
    st.write("### 📝 Etapas do Processo")
    
    # Prepara os itens para ordenação
    step_labels = [
        f"{i+1}. {step.get('name', 'Nova Etapa')}"
        for i, step in enumerate(st.session_state.process_steps)
    ]
    
    # Renderiza a lista ordenável
    sorted_indices = sort_items(step_labels)
    
    # Se a ordem mudou, reordena as etapas
    if sorted_indices != step_labels:
        # Extrai os índices originais dos labels ordenados
        original_indices = [
            int(label.split('.')[0]) - 1
            for label in sorted_indices
        ]
        
        # Reordena as etapas
        st.session_state.process_steps = [
            st.session_state.process_steps[i]
            for i in original_indices
        ]
        st.rerun()
    
    # Renderiza os detalhes de cada etapa
    for i, step in enumerate(st.session_state.process_steps):
        with st.container():
            cols = st.columns([8, 1, 1])
            
            with cols[0]:
                st.write(step.get('name', 'Nova Etapa'))
                if step.get('description'):
                    st.caption(
                        step.get('description', '')[:100] + '...' 
                        if len(step.get('description', '')) > 100 
                        else step.get('description', '')
                    )
                if step.get('image'):
                    st.image(step.get('image'), width=100)
            
            with cols[1]:
                if st.button("✏️", key=f"edit_{i}"):
                    render_step_edit_modal(step, i)
            
            with cols[2]:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.process_steps.pop(i)
                    st.rerun()
    
    # Botão para adicionar nova etapa
    if st.button("➕ Nova Etapa", key="add_new"):
        st.session_state.process_steps.append({'name': '', 'description': '', 'image': None})
        st.rerun()
    
    # Modal de edição
    if st.session_state.editing_step is not None:
        with st.form(f"edit_form_{st.session_state.editing_step}"):
            step = st.session_state.process_steps[st.session_state.editing_step]
            
            st.write(f"### Editar Etapa {st.session_state.editing_step + 1}")
            
            step['name'] = st.text_input(
                "Nome da Etapa",
                value=step.get('name', ''),
                placeholder="Ex: Acessar sistema"
            )
            
            step['description'] = st.text_area(
                "Descrição Detalhada",
                value=step.get('description', ''),
                placeholder="Descreva os detalhes desta etapa..."
            )
            
            uploaded_file = st.file_uploader(
                "Imagem da Etapa",
                type=['png', 'jpg', 'jpeg']
            )
            
            if uploaded_file:
                step['image'] = uploaded_file.getvalue()
                st.image(step['image'], caption="Preview da Imagem")
            elif step.get('image'):
                st.image(step['image'], caption="Imagem Atual")
            
            if st.form_submit_button("Salvar"):
                st.session_state.editing_step = None
                st.rerun()
    
    # Formulário principal
    with st.form("details_form"):
        # Sistemas e Ferramentas
        st.write("### 🔧 Sistemas e Ferramentas")
        
        # Sistemas Comuns (Predefinidos)
        st.write("**Sistemas Comuns**")
        common_tools = st.multiselect(
            "Selecione os sistemas predefinidos:",
            OPTIONS['systems']['common_tools'],
            default=initial_data.get('tools', {}).get('common_tools', []),
            help="Selecione os sistemas comumente utilizados na empresa"
        )
        
        st.divider()
        
        # Sistemas Customizados
        st.write("**Sistemas Customizados**")
        
        # Lista de sistemas customizados
        custom_tools = []
        for i, tool in enumerate(st.session_state.custom_tools):
            cols = st.columns([8, 4])
            with cols[0]:
                tool_name = st.text_input(
                    f"Sistema {i+1}",
                    value=tool.get('name', ''),
                    key=f"custom_tool_{i}",
                    placeholder="Nome do sistema customizado"
                )
            with cols[1]:
                tool_desc = st.text_input(
                    "Descrição",
                    value=tool.get('description', ''),
                    key=f"custom_tool_desc_{i}",
                    placeholder="Finalidade do sistema"
                )
            if tool_name:
                custom_tools.append({
                    'name': tool_name,
                    'description': tool_desc
                })
        
        # Botão para adicionar novo sistema
        if st.form_submit_button("➕ Adicionar Sistema"):
            st.session_state.custom_tools.append({'name': ''})
            st.rerun()
        
        st.divider()
        
        # Seção 3: Dados do Processo
        st.write("### 📊 Dados do Processo")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Tipos e Formatos**")
            data_types = st.multiselect(
                "Tipos de Dados:",
                OPTIONS['data_types'],
                default=initial_data.get('data_types', [])
            )
            
            data_formats = st.multiselect(
                "Formatos de Dados:",
                OPTIONS['data_formats'],
                default=initial_data.get('data_formats', [])
            )
        
        with col2:
            st.write("**Fontes e Volume**")
            data_sources = st.multiselect(
                "Fontes de Dados:",
                OPTIONS['data_sources'],
                default=initial_data.get('data_sources', [])
            )
            
            data_volume = st.select_slider(
                "Volume de Dados:",
                options=['Baixo', 'Médio', 'Alto'],
                value=initial_data.get('data_volume', 'Médio')
            )
        
        # Botão de Salvar
        if st.form_submit_button("💾 Salvar Detalhes do Processo"):
            # Remove sistemas vazios
            st.session_state.custom_tools = [
                tool for tool in st.session_state.custom_tools 
                if tool.get('name', '').strip()
            ]
            
            data = {
                "steps": st.session_state.process_steps,
                "tools": {
                    "common_tools": common_tools,
                    "custom_tools": [tool['name'] for tool in custom_tools if tool['name'].strip()]
                },
                "data_types": data_types,
                "data_formats": data_formats,
                "data_sources": data_sources,
                "data_volume": data_volume
            }
            
            if validate_and_submit(data, ["steps"], on_submit):
                st.success("✅ Detalhes do processo salvos com sucesso!")

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