"""Componente para preview de dados em tempo real."""
from typing import Dict, Any, Optional
import streamlit as st
from views.components.state.state_manager import StateManager

class DataPreview:
    """Componente para mostrar preview dos dados em tempo real."""
    
    def __init__(self, form_id: str):
        """
        Inicializa o componente de preview.
        
        Args:
            form_id: ID do formulário
        """
        self.form_id = form_id
        self.state_manager = StateManager()
    
    def render(self, data: Dict[str, Any], show_all: bool = False) -> None:
        """
        Renderiza o preview dos dados.
        
        Args:
            data: Dados para mostrar
            show_all: Se deve mostrar todos os campos ou apenas os preenchidos
        """
        with st.expander("👁️ Preview dos Dados", expanded=False):
            # Remove campos vazios se show_all=False
            preview_data = data if show_all else {
                k: v for k, v in data.items() 
                if v and str(v).strip()
            }
            
            if not preview_data:
                st.info("Nenhum dado preenchido ainda")
                return
                
            # Renderiza os dados em formato amigável
            for field, value in preview_data.items():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(f"**{field.replace('_', ' ').title()}:**")
                with col2:
                    st.write(str(value)) 