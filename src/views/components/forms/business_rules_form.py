"""Formulário de regras de negócio."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class BusinessRulesForm:
    """Formulário de regras de negócio."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "rules"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa lista de regras se necessário
        if "rules_list" not in st.session_state:
            st.session_state.rules_list = self.form_data.data.get("rules", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        rules = data.get("rules", [])
        
        if not rules:
            st.error("Adicione pelo menos uma regra de negócio")
            return False
        
        for rule in rules:
            if not rule.get("description"):
                st.error("Todas as regras precisam ter uma descrição")
                return False
            if not rule.get("type"):
                st.error("Todas as regras precisam ter um tipo")
                return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "rules": st.session_state.rules_list,
            "exceptions": st.session_state.get("exceptions", ""),
            "validations": st.session_state.get("validations", ""),
            "dependencies": st.session_state.get("dependencies", "")
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
    
    def _add_rule(self, description: str, rule_type: str, priority: str) -> None:
        """
        Adiciona uma nova regra à lista.
        
        Args:
            description: Descrição da regra
            rule_type: Tipo da regra
            priority: Prioridade da regra
        """
        if not description:
            st.error("Descrição da regra é obrigatória")
            return
            
        if not rule_type:
            st.error("Tipo da regra é obrigatório")
            return
        
        new_rule = {
            "description": description,
            "type": rule_type,
            "priority": priority
        }
        
        st.session_state.rules_list.append(new_rule)
        st.session_state.new_rule_description = ""
        st.session_state.new_rule_type = ""
        st.session_state.new_rule_priority = "Média"
    
    def _remove_rule(self, index: int) -> None:
        """
        Remove uma regra da lista.
        
        Args:
            index: Índice da regra a ser removida
        """
        st.session_state.rules_list.pop(index)
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📜 Regras de Negócio")
        
        # Adicionar nova regra
        st.write("#### Adicionar Nova Regra")
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            description = st.text_input(
                "Descrição da Regra",
                key="new_rule_description",
                help="Descreva a regra de negócio"
            )
        
        with col2:
            rule_type = st.selectbox(
                "Tipo",
                options=["Validação", "Cálculo", "Decisão", "Processo", "Outro"],
                key="new_rule_type",
                help="Tipo da regra"
            )
        
        with col3:
            priority = st.selectbox(
                "Prioridade",
                options=["Alta", "Média", "Baixa"],
                key="new_rule_priority",
                help="Prioridade da regra"
            )
        
        if st.button("➕ Adicionar Regra", use_container_width=True):
            self._add_rule(description, rule_type, priority)
            st.rerun()
        
        # Lista de regras
        st.write("#### Regras Cadastradas")
        for i, rule in enumerate(st.session_state.rules_list):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{rule['type']}** ({rule['priority']})")
                    st.write(rule['description'])
                
                with col2:
                    if st.button("🗑️", key=f"del_rule_{i}"):
                        self._remove_rule(i)
                        st.rerun()
                
                st.divider()
        
        # Informações adicionais
        st.text_area(
            "Exceções",
            key="exceptions",
            value=self.form_data.data.get("exceptions", ""),
            help="Liste as exceções às regras"
        )
        
        st.text_area(
            "Validações",
            key="validations",
            value=self.form_data.data.get("validations", ""),
            help="Descreva as validações necessárias"
        )
        
        st.text_area(
            "Dependências",
            key="dependencies",
            value=self.form_data.data.get("dependencies", ""),
            help="Liste dependências entre as regras"
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
                st.session_state.rules_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.rules_list = []
                st.warning("Edição cancelada")
                st.rerun() 