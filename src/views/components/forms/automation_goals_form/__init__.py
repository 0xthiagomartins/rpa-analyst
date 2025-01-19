# Package marker """Formulário de objetivos da automação."""
from typing import Dict, Any, List
import streamlit as st
from src.utils.logger import Logger
from ..form_base import SuggestibleForm

class AutomationGoalsForm(SuggestibleForm):
    """Formulário de objetivos da automação."""
    
    def __init__(self):
        """Inicializa o formulário."""
        super().__init__("automation_goals")
        self.logger = Logger()

    def apply_suggestions(self, data: Dict[str, Any]):
        """Aplica as sugestões ao formulário."""
        st.session_state["automation_goals"] = data.get("automation_goals", []).copy()
        st.session_state["success_metrics"] = data.get("success_metrics", []).copy()

    async def render(self):
        """Renderiza o formulário."""
        st.write("### 🎯 Objetivos da Automação")
        needs_rerun = False
        
        # Seção de Objetivos
        st.write("#### Objetivos Principais")
        goals = st.session_state.get('automation_goals', [])
        
        for i, goal in enumerate(goals):
            col1, col2 = st.columns([4, 1])
            with col1:
                updated_goal = st.text_area(
                    f"Objetivo {i+1}",
                    value=goal,
                    key=f"goal_{i}"
                )
                if updated_goal != goal:
                    goals[i] = updated_goal
                    st.session_state.automation_goals = goals
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_goal_{i}"):
                    goals.pop(i)
                    st.session_state.automation_goals = goals
                    needs_rerun = True
        
        # Botão para adicionar objetivo
        if st.button("➕ Adicionar Objetivo"):
            goals.append("")
            st.session_state.automation_goals = goals
            needs_rerun = True
        
        # Seção de Métricas
        st.write("#### Métricas de Sucesso")
        metrics = st.session_state.get('success_metrics', [])
        
        for i, metric in enumerate(metrics):
            col1, col2 = st.columns([4, 1])
            with col1:
                updated_metric = st.text_input(
                    f"Métrica {i+1}",
                    value=metric,
                    key=f"metric_{i}"
                )
                if updated_metric != metric:
                    metrics[i] = updated_metric
                    st.session_state.success_metrics = metrics
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_metric_{i}"):
                    metrics.pop(i)
                    st.session_state.success_metrics = metrics
                    needs_rerun = True
        
        # Botão para adicionar métrica
        if st.button("➕ Adicionar Métrica"):
            metrics.append("")
            st.session_state.success_metrics = metrics
            needs_rerun = True
        
        # Renderiza sugestões se disponíveis
        await self.render_suggestions()
        
        # Rerun apenas se necessário
        if needs_rerun:
            st.rerun() 