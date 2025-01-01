"""Formulário de objetivos e KPIs."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.forms.form_base import BaseForm
from views.components.forms.form_field import FormField

class GoalsForm(BaseForm):
    """Formulário para objetivos e KPIs."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("goals", container)
        
        # Inicializa campos
        self.goals_field = FormField(self.form_id, "goals")
        self.kpis_field = FormField(self.form_id, "kpis")
        
        # Inicializa listas se não existirem
        if "goals_list" not in st.session_state:
            st.session_state.goals_list = self.form_data.data.get("goals", [])
        if "kpis_list" not in st.session_state:
            st.session_state.kpis_list = self.form_data.data.get("kpis", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida objetivos
        if not st.session_state.goals_list:
            errors.append("Pelo menos um objetivo é obrigatório")
            is_valid = False
        
        # Valida KPIs
        if not st.session_state.kpis_list:
            errors.append("Pelo menos um KPI é obrigatório")
            is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_goal(self) -> None:
        """Adiciona um novo objetivo."""
        new_goal = st.text_area("Novo Objetivo", key="new_goal")
        if st.button("➕ Adicionar Objetivo"):
            if new_goal:
                st.session_state.goals_list.append(new_goal)
                self.update_field("goals", st.session_state.goals_list)
                st.rerun()
    
    def _add_kpi(self) -> None:
        """Adiciona um novo KPI."""
        col1, col2 = st.columns(2)
        with col1:
            metric = st.text_input("Métrica", key="new_kpi_metric")
        with col2:
            target = st.text_input("Meta", key="new_kpi_target")
            
        if st.button("➕ Adicionar KPI"):
            if metric and target:
                new_kpi = {"metric": metric, "target": target}
                st.session_state.kpis_list.append(new_kpi)
                self.update_field("kpis", st.session_state.kpis_list)
                st.rerun()
            else:
                st.error("Preencha a métrica e a meta")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("🎯 Objetivos e KPIs")
        
        # Seção de Objetivos
        st.write("#### Objetivos")
        
        # Lista objetivos existentes
        for i, goal in enumerate(st.session_state.goals_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_goal = st.text_area(
                    f"Objetivo {i+1}",
                    value=goal,
                    key=f"goal_{i}",
                    disabled=not self.is_editing
                )
                if self.is_editing and new_goal != goal:
                    st.session_state.goals_list[i] = new_goal
                    self.update_field("goals", st.session_state.goals_list)
            
            with col2:
                if self.is_editing and st.button("🗑️", key=f"del_goal_{i}"):
                    st.session_state.goals_list.pop(i)
                    self.update_field("goals", st.session_state.goals_list)
                    st.rerun()
        
        # Adicionar novo objetivo
        if self.is_editing:
            self._add_goal()
        
        # Seção de KPIs
        st.write("#### KPIs")
        
        # Lista KPIs existentes
        for i, kpi in enumerate(st.session_state.kpis_list):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_metric = st.text_input(
                    "Métrica",
                    value=kpi["metric"],
                    key=f"kpi_metric_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_target = st.text_input(
                    "Meta",
                    value=kpi["target"],
                    key=f"kpi_target_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_kpi_{i}"):
                    st.session_state.kpis_list.pop(i)
                    self.update_field("kpis", st.session_state.kpis_list)
                    st.rerun()
            
            if self.is_editing and (new_metric != kpi["metric"] or new_target != kpi["target"]):
                st.session_state.kpis_list[i] = {
                    "metric": new_metric,
                    "target": new_target
                }
                self.update_field("kpis", st.session_state.kpis_list)
        
        # Adicionar novo KPI
        if self.is_editing:
            self._add_kpi()