"""Formulário de regras de negócio."""
from typing import Dict, Any, List
import streamlit as st
from src.utils.logger import Logger
from .form_base import SuggestibleForm

class BusinessRulesForm(SuggestibleForm):
    """Formulário de regras de negócio."""
    
    def __init__(self):
        """Inicializa o formulário."""
        super().__init__("business_rules")
        self.logger = Logger()

    def apply_suggestions(self, data: Dict[str, Any]):
        """Aplica as sugestões ao formulário."""
        st.session_state["business_rules"] = data.get("business_rules", []).copy()
        st.session_state["exceptions"] = data.get("exceptions", []).copy()

    async def render(self):
        """Renderiza o formulário."""
        st.write("### 📜 Regras de Negócio")
        needs_rerun = False
        
        # Lista de regras
        st.write("#### Regras de Negócio")
        rules = st.session_state.get("business_rules", [])
        
        # Renderiza todas as regras primeiro
        for i in range(len(rules)):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_rule = st.text_area(
                    f"Regra {i+1}",
                    value=rules[i],
                    key=f"rule_{i}",
                    on_change=lambda: None
                )
                if new_rule != rules[i]:
                    rules[i] = new_rule
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_rule_{i}"):
                    rules.pop(i)
                    needs_rerun = True
        
        # Botão para adicionar regra
        if st.button("➕ Adicionar Regra"):
            rules.append("")
            needs_rerun = True
            
        # Lista de exceções
        st.write("#### Exceções")
        exceptions = st.session_state.get("exceptions", [])
        
        # Depois renderiza todas as exceções
        for i in range(len(exceptions)):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_exception = st.text_area(
                    f"Exceção {i+1}",
                    value=exceptions[i],
                    key=f"exception_{i}",
                    on_change=lambda: None
                )
                if new_exception != exceptions[i]:
                    exceptions[i] = new_exception
                    needs_rerun = True
            
            with col2:
                if st.button("🗑️", key=f"del_exception_{i}"):
                    exceptions.pop(i)
                    needs_rerun = True
        
        # Botão para adicionar exceção
        if st.button("➕ Adicionar Exceção"):
            exceptions.append("")
            needs_rerun = True
            
        # Atualiza session_state
        st.session_state["business_rules"] = rules
        st.session_state["exceptions"] = exceptions
        
        # Renderiza sugestões se disponíveis
        await self.render_suggestions()
        
        # Rerun apenas se necessário
        if needs_rerun:
            st.rerun() 