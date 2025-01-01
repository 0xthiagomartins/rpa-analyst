"""Formulário de detalhes do processo."""
from typing import Optional, Dict, Any
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class ProcessDetailsForm:
    """Formulário de detalhes do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "details"
        
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
        if not data.get("current_process"):
            st.error("Descrição do processo atual é obrigatória")
            return False
            
        if not data.get("pain_points"):
            st.error("Pontos de dor são obrigatórios")
            return False
            
        if not data.get("expected_benefits"):
            st.error("Benefícios esperados são obrigatórios")
            return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "current_process": st.session_state.get("current_process", ""),
            "pain_points": st.session_state.get("pain_points", ""),
            "expected_benefits": st.session_state.get("expected_benefits", ""),
            "stakeholders": st.session_state.get("stakeholders", ""),
            "constraints": st.session_state.get("constraints", ""),
            "additional_info": st.session_state.get("additional_info", "")
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
        st.write("### 📋 Detalhes do Processo")
        
        # Processo atual
        st.text_area(
            "Processo Atual",
            key="current_process",
            value=self.form_data.data.get("current_process", ""),
            help="Descreva como o processo é executado atualmente",
            height=150
        )
        
        # Pontos de dor e benefícios
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Pontos de Dor",
                key="pain_points",
                value=self.form_data.data.get("pain_points", ""),
                help="Liste os principais problemas do processo atual",
                height=150
            )
        
        with col2:
            st.text_area(
                "Benefícios Esperados",
                key="expected_benefits",
                value=self.form_data.data.get("expected_benefits", ""),
                help="Descreva os benefícios esperados com a automação",
                height=150
            )
        
        # Stakeholders e restrições
        st.text_area(
            "Stakeholders",
            key="stakeholders",
            value=self.form_data.data.get("stakeholders", ""),
            help="Liste as pessoas/áreas envolvidas no processo"
        )
        
        st.text_area(
            "Restrições",
            key="constraints",
            value=self.form_data.data.get("constraints", ""),
            help="Liste restrições ou limitações do processo"
        )
        
        # Informações adicionais
        st.text_area(
            "Informações Adicionais",
            key="additional_info",
            value=self.form_data.data.get("additional_info", ""),
            help="Outras informações relevantes"
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