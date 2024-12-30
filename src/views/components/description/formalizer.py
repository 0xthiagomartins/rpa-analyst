"""Módulo do formalizador de descrições."""
from typing import Optional, Callable
import streamlit as st
from src.services.ai_service import AIService
from src.utils.config_constants import UI_CONFIG
from src.utils.dependency_container import DependencyContainer

class DescriptionFormalizer:
    """Classe para gerenciar a formalização de descrições."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa o formalizador."""
        self.container = container or DependencyContainer()
        self.ai_service = self.container.resolve(AIService)
        self._original_text = ""
        self._formalized_text = ""
        self._preview_enabled = True
        self._history = []  # Lista de tuplas (original, formalizado)
        
    @property
    def original_text(self) -> str:
        """Retorna o texto original."""
        return self._original_text
        
    @property
    def formalized_text(self) -> str:
        """Retorna o texto formalizado."""
        return self._formalized_text
        
    def formalize(self, text: str) -> bool:
        """Formaliza o texto usando IA."""
        try:
            if not text or not text.strip():
                return False
                
            # Valida tamanho do texto
            if len(text) > UI_CONFIG['MAX_DESCRIPTION_LENGTH']:
                st.error(f"Texto muito longo. Máximo: {UI_CONFIG['MAX_DESCRIPTION_LENGTH']} caracteres")
                return False
                
            result = self.ai_service.formalize_description(text)
            if not result:
                return False
                
            self._original_text = text.strip()
            self._formalized_text = result.strip()
            
            # Adiciona ao histórico
            self._history.append((self._original_text, self._formalized_text))
            
            return True
        except Exception as e:
            st.error(f"Erro ao formalizar texto: {str(e)}")
            return False
            
    def clear(self) -> None:
        """Limpa os textos."""
        self._original_text = ""
        self._formalized_text = ""
            
    def render(self, on_save: Optional[Callable] = None) -> None:
        """Renderiza o formalizador."""
        st.write("### 📝 Formalizador de Descrição")
        
        # Entrada do texto original
        col1, col2 = st.columns([3, 1])
        with col1:
            new_text = st.text_area(
                "Texto Original",
                value=self._original_text,
                height=200,
                max_chars=UI_CONFIG['MAX_DESCRIPTION_LENGTH'],
                help=f"Máximo: {UI_CONFIG['MAX_DESCRIPTION_LENGTH']} caracteres"
            )
            if new_text != self._original_text:
                self._original_text = new_text
                self._formalized_text = ""  # Limpa texto formalizado quando original muda
        
        with col2:
            st.write("#### Controles")
            self._preview_enabled = st.toggle("Preview", value=self._preview_enabled)
            
            if st.button("✨ Formalizar", use_container_width=True):
                if self.formalize(self._original_text):
                    st.success("Texto formalizado!")
                    
                    if self._preview_enabled:
                        st.write("#### Resultado")
                        st.info(self._formalized_text)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Aceitar", use_container_width=True):
                                if on_save:
                                    on_save(self._formalized_text)
                                    st.success("Texto salvo!")
                        with col2:
                            if st.button("❌ Rejeitar", use_container_width=True):
                                self._formalized_text = ""
                                st.info("Texto rejeitado")
        
        # Mostra histórico se houver
        if self._history and self._preview_enabled:
            st.write("#### Histórico")
            for i, (orig, form) in enumerate(reversed(self._history[-3:])):  # Mostra últimos 3
                with st.expander(f"Versão {len(self._history) - i}"):
                    st.write("**Original:**")
                    st.text(orig)
                    st.write("**Formalizado:**")
                    st.text(form) 