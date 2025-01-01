"""Formulário de objetivos da automação."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class AutomationGoalsForm:
    """Formulário de objetivos da automação."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "automation"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa lista de objetivos se necessário
        if "goals_list" not in st.session_state:
            st.session_state.goals_list = self.form_data.data.get("goals", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        goals = data.get("goals", [])
        
        if not goals:
            st.error("Adicione pelo menos um objetivo")
            return False
        
        for goal in goals:
            if not goal.get("description"):
                st.error("Todos os objetivos precisam ter uma descrição")
                return False
            if not goal.get("metric"):
                st.error("Todos os objetivos precisam ter uma métrica")
                return False
        
        if not data.get("scope"):
            st.error("Defina o escopo da automação")
            return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "goals": st.session_state.goals_list,
            "scope": st.session_state.get("scope", ""),
            "constraints": st.session_state.get("constraints", ""),
            "success_criteria": st.session_state.get("success_criteria", ""),
            "risks": st.session_state.get("risks", ""),
            "assumptions": st.session_state.get("assumptions", "")
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
    
    def _add_goal(self, description: str, metric: str, target: str) -> None:
        """
        Adiciona um novo objetivo à lista.
        
        Args:
            description: Descrição do objetivo
            metric: Métrica de medição
            target: Meta a ser alcançada
        """
        if not description:
            st.error("Descrição do objetivo é obrigatória")
            return
            
        if not metric:
            st.error("Métrica é obrigatória")
            return
        
        new_goal = {
            "description": description,
            "metric": metric,
            "target": target
        }
        
        st.session_state.goals_list.append(new_goal)
        st.session_state.new_goal_description = ""
        st.session_state.new_goal_metric = ""
        st.session_state.new_goal_target = ""
    
    def _remove_goal(self, index: int) -> None:
        """
        Remove um objetivo da lista.
        
        Args:
            index: Índice do objetivo a ser removido
        """
        st.session_state.goals_list.pop(index)
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 🎯 Objetivos da Automação")
        
        # Adicionar novo objetivo
        st.write("#### Adicionar Novo Objetivo")
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            description = st.text_input(
                "Descrição do Objetivo",
                key="new_goal_description",
                help="Descreva o objetivo da automação"
            )
        
        with col2:
            metric = st.text_input(
                "Métrica",
                key="new_goal_metric",
                help="Como será medido"
            )
        
        with col3:
            target = st.text_input(
                "Meta",
                key="new_goal_target",
                help="Valor a ser alcançado"
            )
        
        if st.button("➕ Adicionar Objetivo", use_container_width=True):
            self._add_goal(description, metric, target)
            st.rerun()
        
        # Lista de objetivos
        st.write("#### Objetivos Cadastrados")
        for i, goal in enumerate(st.session_state.goals_list):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{goal['description']}**")
                    st.write(f"Métrica: {goal['metric']} | Meta: {goal['target']}")
                
                with col2:
                    if st.button("🗑️", key=f"del_goal_{i}"):
                        self._remove_goal(i)
                        st.rerun()
                
                st.divider()
        
        # Informações adicionais
        st.text_area(
            "Escopo da Automação",
            key="scope",
            value=self.form_data.data.get("scope", ""),
            help="Defina o escopo e limites da automação",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Restrições",
                key="constraints",
                value=self.form_data.data.get("constraints", ""),
                help="Liste as restrições da automação"
            )
            
            st.text_area(
                "Critérios de Sucesso",
                key="success_criteria",
                value=self.form_data.data.get("success_criteria", ""),
                help="Defina os critérios de sucesso"
            )
        
        with col2:
            st.text_area(
                "Riscos",
                key="risks",
                value=self.form_data.data.get("risks", ""),
                help="Liste os riscos identificados"
            )
            
            st.text_area(
                "Premissas",
                key="assumptions",
                value=self.form_data.data.get("assumptions", ""),
                help="Liste as premissas consideradas"
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
                st.session_state.goals_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.goals_list = []
                st.warning("Edição cancelada")
                st.rerun() 