"""Módulo do formulário de objetivos da automação."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class AutomationGoalsForm(FormBase):
    """Formulário para objetivos e KPIs da automação."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "automation_goals")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_goal(self, goals: List[str]) -> None:
        """Adiciona um novo objetivo."""
        new_goal = st.text_area(
            "Novo Objetivo",
            key="new_goal",
            help="Descreva um objetivo da automação"
        )
        if st.button("➕ Adicionar Objetivo") and new_goal:
            goals.append(new_goal)
    
    def _add_kpi(self, kpis: List[Dict[str, str]]) -> None:
        """Adiciona um novo KPI."""
        col1, col2 = st.columns(2)
        with col1:
            metric = st.text_input(
                "Métrica",
                key="new_kpi_metric",
                help="Nome da métrica"
            )
        with col2:
            target = st.text_input(
                "Meta",
                key="new_kpi_target",
                help="Valor alvo"
            )
            
        if st.button("➕ Adicionar KPI") and metric and target:
            kpis.append({
                "metric": metric,
                "target": target
            })
        
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 🎯 Objetivos da Automação")
        
        # Inicializa listas se não existirem
        if "automation_goals" not in self._data:
            self._data["automation_goals"] = []
        if "kpis" not in self._data:
            self._data["kpis"] = []
            
        # Seção de Objetivos
        st.write("#### Objetivos")
        goals = self._data["automation_goals"]
        
        # Lista objetivos existentes
        for i, goal in enumerate(goals):
            col1, col2 = st.columns([4, 1])
            with col1:
                goals[i] = st.text_area(f"Objetivo {i+1}", value=goal, key=f"goal_{i}")
            with col2:
                if st.button("🗑️", key=f"del_goal_{i}"):
                    goals.pop(i)
                    st.rerun()
        
        # Adicionar novo objetivo
        self._add_goal(goals)
        
        # Seção de KPIs
        st.write("#### KPIs")
        kpis = self._data["kpis"]
        
        # Lista KPIs existentes
        for i, kpi in enumerate(kpis):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                kpis[i]["metric"] = st.text_input(
                    "Métrica",
                    value=kpi["metric"],
                    key=f"kpi_metric_{i}"
                )
            with col2:
                kpis[i]["target"] = st.text_input(
                    "Meta",
                    value=kpi["target"],
                    key=f"kpi_target_{i}"
                )
            with col3:
                if st.button("🗑️", key=f"del_kpi_{i}"):
                    kpis.pop(i)
                    st.rerun()
        
        # Adicionar novo KPI
        self._add_kpi(kpis) 