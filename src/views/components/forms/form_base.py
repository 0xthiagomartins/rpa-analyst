"""Classe base para formulários."""
from typing import Dict, Any, List
import streamlit as st
from src.views.components.state.suggestions_buffer import SuggestionsState

class SuggestibleForm:
    """Classe base para formulários que podem receber sugestões."""
    
    def __init__(self, form_id: str):
        """Inicializa o formulário."""
        self.form_id = form_id
        
    def get_data(self) -> Dict[str, Any]:
        """Retorna os dados do formulário."""
        return {}
        
    def apply_suggestions(self, data: Dict[str, Any]):
        """Aplica as sugestões ao formulário."""
        pass
        
    async def render_suggestions(self):
        """Renderiza as sugestões disponíveis."""
        buffer = SuggestionsState.get_buffer()
        if buffer and self.form_id in buffer.forms_data:
            st.write("### 💡 Sugestões Disponíveis")
            st.write("Dados sugeridos:")
            
            form_data = buffer.forms_data[self.form_id]["data"]
            st.write(form_data)
            
            if st.button("✅ Aplicar Sugestões", key=f"apply_{self.form_id}"):
                self.apply_suggestions(form_data)
                st.rerun()
    
    async def render(self):
        """Renderiza o formulário."""
        pass 