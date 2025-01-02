"""Formulário de objetivos da automação."""
from typing import Dict, Any, List
import streamlit as st
from src.utils.logger import Logger
from .form_base import SuggestibleForm

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
        
        # Objetivos principais
        st.write("#### Objetivos Principais")
        goals = st.session_state.get("automation_goals", [])
        
        # Renderiza todos os objetivos primeiro
        for i in range(len(goals)):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_goal = st.text_area(
                    f"Objetivo {i+1}",
                    value=goals[i],
                    key=f"goal_{i}",
                    on_change=lambda: None
                )
                if new_goal != goals[i]:
                    goals[i] = new_goal
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_goal_{i}"):
                    goals.pop(i)
                    needs_rerun = True
        
        # Botão para adicionar objetivo
        if st.button("➕ Adicionar Objetivo"):
            goals.append("")
            needs_rerun = True
            
        # Métricas de sucesso
        st.write("#### Métricas de Sucesso")
        metrics = st.session_state.get("success_metrics", [])
        
        # Depois renderiza todas as métricas
        for i in range(len(metrics)):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_metric = st.text_area(
                    f"Métrica {i+1}",
                    value=metrics[i],
                    key=f"metric_{i}",
                    on_change=lambda: None
                )
                if new_metric != metrics[i]:
                    metrics[i] = new_metric
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_metric_{i}"):
                    metrics.pop(i)
                    needs_rerun = True
        
        # Botão para adicionar métrica
        if st.button("➕ Adicionar Métrica"):
            metrics.append("")
            needs_rerun = True
            
        # Atualiza session_state
        st.session_state["automation_goals"] = goals
        st.session_state["success_metrics"] = metrics
        
        # Renderiza sugestões se disponíveis
        await self.render_suggestions()
        
        # Rerun apenas se necessário
        if needs_rerun:
            st.rerun() 