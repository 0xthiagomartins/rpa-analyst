"""Formulário de detalhes do processo."""
import streamlit as st
from typing import Dict, Any
from src.utils.logger import Logger
from .form_base import SuggestibleForm

class ProcessDetailsForm(SuggestibleForm):
    """Formulário de detalhes do processo."""
    
    def __init__(self):
        """Inicializa o formulário."""
        super().__init__("process_details")
        self.logger = Logger()

    async def render(self):
        """Renderiza o formulário."""
        st.write("### 📋 Detalhes do Processo")
        
        # Campos do formulário
        objective = st.text_area(
            "Objetivo do Processo",
            value=st.session_state.get("process_objective", ""),
            help="Descreva o objetivo principal do processo"
        )
        
        scope = st.text_area(
            "Escopo",
            value=st.session_state.get("process_scope", ""),
            help="Defina o escopo e limites do processo"
        )
        
        frequency = st.selectbox(
            "Frequência de Execução",
            options=["Diário", "Semanal", "Mensal", "Sob Demanda"],
            index=0 if not st.session_state.get("frequency") else 
                  ["Diário", "Semanal", "Mensal", "Sob Demanda"].index(
                      st.session_state.get("frequency")
                  )
        )
        
        volume = st.number_input(
            "Volume Mensal",
            min_value=0,
            value=st.session_state.get("monthly_volume", 0),
            help="Quantidade média de execuções por mês"
        )
        
        time_per_execution = st.number_input(
            "Tempo por Execução (minutos)",
            min_value=0,
            value=st.session_state.get("time_per_execution", 0),
            help="Tempo médio gasto em cada execução"
        )
        
        data_used = st.text_area(
            "Dados Utilizados",
            value=st.session_state.get("data_used", ""),
            help="Descreva os dados manipulados no processo"
        )
        
        # Atualiza session_state
        st.session_state.update({
            'process_objective': objective,
            'process_scope': scope,
            'frequency': frequency,
            'monthly_volume': volume,
            'time_per_execution': time_per_execution,
            'data_used': data_used
        })
        
        # Renderiza sugestões se disponíveis
        await self.render_suggestions() 