"""Módulo do editor de diagramas."""
from typing import Dict, List, Optional, Callable
import streamlit as st
from src.services.ai_service import AIService
from src.utils.validators import validate_diagram

class DiagramEditor:
    """Classe para gerenciar o editor de diagramas."""
    
    def __init__(self, ai_service: Optional[AIService] = None):
        """Inicializa o editor de diagramas."""
        self.ai_service = ai_service or AIService()
        self._diagram_code = ""
        self._preview_enabled = True
        
    @property
    def diagram_code(self) -> str:
        """Retorna o código do diagrama atual."""
        return self._diagram_code
        
    @diagram_code.setter
    def diagram_code(self, value: str) -> None:
        """Define o código do diagrama."""
        if not validate_diagram(value):
            raise ValueError("Código do diagrama inválido")
        self._diagram_code = value
        
    def generate_from_description(self, description: str, steps: List[str]) -> bool:
        """Gera diagrama a partir da descrição e passos."""
        try:
            result = self.ai_service.generate_diagram(description, steps)
            self.diagram_code = result.code
            return True
        except Exception as e:
            st.error(f"Erro ao gerar diagrama: {str(e)}")
            return False
            
    def render(self, on_save: Optional[Callable] = None) -> None:
        """Renderiza o editor de diagramas."""
        st.write("### 📊 Editor de Diagrama")
        
        # Controles do editor
        col1, col2 = st.columns([3, 1])
        with col1:
            self._diagram_code = st.text_area(
                "Código Mermaid",
                value=self._diagram_code,
                height=300
            )
        
        with col2:
            st.write("#### Controles")
            self._preview_enabled = st.toggle("Preview", value=self._preview_enabled)
            
            if st.button("💾 Salvar", use_container_width=True):
                if on_save and validate_diagram(self._diagram_code):
                    on_save(self._diagram_code)
                    st.success("Diagrama salvo!")
                else:
                    st.error("Diagrama inválido")
        
        # Preview do diagrama
        if self._preview_enabled and self._diagram_code:
            st.write("#### Preview")
            st.mermaid(self._diagram_code) 