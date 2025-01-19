"""View principal da aplicação."""
import streamlit as st
from typing import Optional
from .components.forms.identification_form import IdentificationForm
from .components.process.timeline import ProcessTimeline

class MainView:
    """Classe principal da interface."""
    
    def __init__(self):
        """Inicializa a view principal."""
        self.timeline = ProcessTimeline()
        self.current_form = IdentificationForm()
    
    async def render(self) -> None:
        """Renderiza a interface principal."""
        st.title("🤖 RPA Analyst")
        
        # Renderiza timeline
        self.timeline.render()
        
        st.write("---")
        
        # Renderiza formulário atual
        await self.current_form.render() 