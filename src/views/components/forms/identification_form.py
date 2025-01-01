"""Formulário de identificação do processo."""
from typing import Optional, Dict, Any
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class IdentificationForm:
    """Formulário de identificação do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "identification"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        
        # Validações básicas
        if not data.get("process_name"):
            st.error("Nome do processo é obrigatório")
            return False
            
        if not data.get("process_owner"):
            st.error("Responsável é obrigatório")
            return False
            
        if not data.get("department"):
            st.error("Departamento é obrigatório")
            return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "process_name": st.session_state.get("process_name", ""),
            "process_owner": st.session_state.get("process_owner", ""),
            "department": st.session_state.get("department", ""),
            "priority": st.session_state.get("priority", ""),
            "status": st.session_state.get("status", ""),
            "description": st.session_state.get("description", "")
        }
    
    def save(self) -> bool:
        """
        Salva os dados do formulário.
        
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        data = self.get_data()
        is_valid = self.validate()
        
        # Atualiza estado
        self.state_manager.update_form_data(
            self.form_id,
            data=data,
            is_valid=is_valid,
            state=FormState.COMPLETED if is_valid else FormState.INVALID
        )
        
        return is_valid
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 🎯 Identificação do Processo")
        
        # Dados básicos
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input(
                "Nome do Processo",
                key="process_name",
                value=self.form_data.data.get("process_name", ""),
                help="Nome do processo a ser automatizado"
            )
            
            st.text_input(
                "Responsável",
                key="process_owner",
                value=self.form_data.data.get("process_owner", ""),
                help="Responsável pelo processo"
            )
        
        with col2:
            st.selectbox(
                "Departamento",
                options=["TI", "RH", "Financeiro", "Comercial", "Operações"],
                key="department",
                index=0 if not self.form_data.data.get("department") else None,
                help="Departamento responsável pelo processo"
            )
            
            st.selectbox(
                "Prioridade",
                options=["Alta", "Média", "Baixa"],
                key="priority",
                index=1 if not self.form_data.data.get("priority") else None,
                help="Prioridade de automação"
            )
        
        # Status e descrição
        st.selectbox(
            "Status",
            options=["Em Análise", "Em Desenvolvimento", "Concluído"],
            key="status",
            index=0 if not self.form_data.data.get("status") else None,
            help="Status atual do processo"
        )
        
        st.text_area(
            "Descrição",
            key="description",
            value=self.form_data.data.get("description", ""),
            help="Breve descrição do processo"
        )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar", use_container_width=True):
                if self.save():
                    st.success("Dados salvos com sucesso!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Limpar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.warning("Edição cancelada")
                st.rerun() 