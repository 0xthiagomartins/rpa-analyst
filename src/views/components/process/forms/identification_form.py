"""Módulo para o formulário de identificação do processo."""
from typing import Dict, Optional, Callable
from datetime import datetime
import streamlit as st
from src.services.ai_service import AIService
from src.views.components.process.config.constants import UI_CONFIG, ERROR_MESSAGES

class IdentificationForm:
    """Classe para gerenciar o formulário de identificação do processo."""
    
    VALID_PRIORITIES = ["Baixa", "Média", "Alta"]
    VALID_COMPLEXITIES = ["Baixa", "Média", "Alta"]
    
    def __init__(self):
        """Inicializa o formulário com valores padrão."""
        self.process_name = ""
        self.process_owner = ""
        self.department = ""
        self.current_status = ""
        self.priority = "Média"
        self.complexity = "Média"
        self.estimated_time = ""
        self.observations = ""
        
    @property
    def priority(self) -> str:
        """Retorna a prioridade do processo."""
        return self._priority
        
    @priority.setter
    def priority(self, value: str) -> None:
        """Define a prioridade do processo."""
        if value not in self.VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida. Valores permitidos: {self.VALID_PRIORITIES}")
        self._priority = value
        
    @property
    def complexity(self) -> str:
        """Retorna a complexidade do processo."""
        return self._complexity
        
    @complexity.setter
    def complexity(self, value: str) -> None:
        """Define a complexidade do processo."""
        if value not in self.VALID_COMPLEXITIES:
            raise ValueError(f"Complexidade inválida. Valores permitidos: {self.VALID_COMPLEXITIES}")
        self._complexity = value
        
    def validate(self) -> bool:
        """Valida se todos os campos obrigatórios estão preenchidos."""
        required_fields = [
            self.process_name,
            self.process_owner,
            self.department,
            self.current_status,
            self.estimated_time
        ]
        return all(field.strip() for field in required_fields)
        
    def to_dict(self) -> Dict:
        """Converte o formulário para um dicionário."""
        return {
            "process_name": self.process_name,
            "process_owner": self.process_owner,
            "department": self.department,
            "current_status": self.current_status,
            "priority": self.priority,
            "complexity": self.complexity,
            "estimated_time": self.estimated_time,
            "observations": self.observations
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'IdentificationForm':
        """Cria uma instância do formulário a partir de um dicionário."""
        form = cls()
        form.process_name = data.get("process_name", "")
        form.process_owner = data.get("process_owner", "")
        form.department = data.get("department", "")
        form.current_status = data.get("current_status", "")
        form.priority = data.get("priority", "Média")
        form.complexity = data.get("complexity", "Média")
        form.estimated_time = data.get("estimated_time", "")
        form.observations = data.get("observations", "")
        return form
        
    def clear(self) -> None:
        """Limpa todos os campos do formulário."""
        self.process_name = ""
        self.process_owner = ""
        self.department = ""
        self.current_status = ""
        self.priority = "Média"
        self.complexity = "Média"
        self.estimated_time = ""
        self.observations = ""

def render_identification_form(
    on_submit: Optional[Callable] = None,
    initial_data: Dict = None,
    key_prefix: str = "identification"
) -> Dict:
    """Renderiza o formulário de identificação do processo."""
    if not initial_data:
        initial_data = {}
    
    st.write("### 🎯 Identificação do Processo")
    
    with st.form(f"{key_prefix}_form"):
        # Nome do processo
        process_name = st.text_input(
            "Nome do Processo *",
            value=initial_data.get('process_name', ''),
            help="Nome descritivo do processo a ser automatizado",
            max_chars=UI_CONFIG['MAX_NAME_LENGTH'],
            key=f"{key_prefix}_name"
        )
        
        # Responsável
        process_owner = st.text_input(
            "Responsável *",
            value=initial_data.get('process_owner', ''),
            help="Nome do responsável pelo processo",
            max_chars=UI_CONFIG['MAX_NAME_LENGTH'],
            key=f"{key_prefix}_owner"
        )
        
        # Descrição
        process_description = st.text_area(
            "Descrição do Processo *",
            value=initial_data.get('process_description', ''),
            help="Descreva o processo em detalhes",
            height=UI_CONFIG['DEFAULT_HEIGHT'],
            max_chars=UI_CONFIG['MAX_DESCRIPTION_LENGTH'],
            key=f"{key_prefix}_description"
        )
        
        # Botões de ação
        col1, col2 = st.columns(UI_CONFIG['COLUMN_WIDTHS']['DEFAULT'])
        with col1:
            submit_clicked = st.form_submit_button(
                "💾 Salvar",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            formalize_clicked = st.form_submit_button(
                "🎩 Formalizar",
                use_container_width=True
            )
        
        # Validação e processamento
        if submit_clicked or formalize_clicked:
            if not all([process_name, process_owner, process_description]):
                st.error(ERROR_MESSAGES['REQUIRED_FIELD'])
                return None
            
            data = {
                "process_name": process_name,
                "process_owner": process_owner,
                "process_description": process_description,
                "created_at": datetime.now().isoformat()
            }
            
            # Se clicou em formalizar, usa a IA para melhorar a descrição
            if formalize_clicked:
                try:
                    with st.spinner("🤖 Formalizando descrição..."):
                        ai_service = AIService()
                        formalized = ai_service.formalize_description(process_description)
                        if formalized:
                            data['process_description'] = formalized
                            st.success("✨ Descrição formalizada com sucesso!")
                            
                            # Mostra comparação
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Original:**")
                                st.info(process_description)
                            with col2:
                                st.write("**Formalizada:**")
                                st.info(formalized)
                            
                            # Botões de aceitar/rejeitar
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Aceitar versão formalizada", use_container_width=True, type="primary"):
                                    if on_submit:
                                        on_submit(data)
                            with col2:
                                if st.button("❌ Rejeitar e manter original", use_container_width=True):
                                    if on_submit:
                                        on_submit({**data, 'process_description': process_description})
                                        
                except Exception as e:
                    st.error(f"❌ Erro ao formalizar descrição: {str(e)}")
            
            # Se clicou em salvar, envia direto
            elif submit_clicked and on_submit:
                on_submit(data)
            
            return data
    
    return None 

@classmethod
def from_dict(cls, data: dict) -> 'IdentificationForm':
    """Cria uma instância do formulário a partir de um dicionário."""
    form = cls()
    form.process_name = data.get("process_name", "")
    form.process_owner = data.get("process_owner", "")
    form.department = data.get("department", "")
    form.current_status = data.get("current_status", "")
    form.priority = data.get("priority", "Média")
    form.complexity = data.get("complexity", "Média")
    form.estimated_time = data.get("estimated_time", "")
    form.observations = data.get("observations", "")
    return form

def clear(self) -> None:
    """Limpa todos os campos do formulário."""
    self.process_name = ""
    self.process_owner = ""
    self.department = ""
    self.current_status = ""
    self.priority = "Média"
    self.complexity = "Média"
    self.estimated_time = ""
    self.observations = "" 