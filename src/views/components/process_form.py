"""Módulo do formulário principal."""
from typing import Dict, Any, Optional, List
import streamlit as st
from utils.container_interface import ContainerInterface
from controllers.process_controller import ProcessController

class ProcessForm:
    """Classe principal do formulário de processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        self.container = container or DependencyContainer()
        self.controller = self.container.resolve(ProcessController)
        self._data: Dict[str, Any] = {}
        self._current_step = 0
        
        # Inicializa estado se necessário
        if 'process_data' not in st.session_state:
            st.session_state.process_data = {}
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📝 Formulário do Processo")
        
        # Tabs principais
        tab_info, tab_details = st.tabs(["ℹ️ Informações Básicas", "📋 Detalhes"])
        
        with tab_info:
            self._render_basic_info()
            
        with tab_details:
            self._render_details()
    
    def _render_basic_info(self) -> None:
        """Renderiza seção de informações básicas."""
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input(
                "Nome do Processo",
                key="process_name",
                value=self._data.get("process_name", ""),
                help="Nome do processo a ser automatizado"
            )
            
            st.text_input(
                "Responsável",
                key="process_owner",
                value=self._data.get("process_owner", ""),
                help="Responsável pelo processo"
            )
        
        with col2:
            st.selectbox(
                "Departamento",
                options=["TI", "RH", "Financeiro", "Comercial", "Operações"],
                key="department",
                index=0 if not self._data.get("department") else None,
                help="Departamento responsável pelo processo"
            )
            
            st.selectbox(
                "Status",
                options=["Em Análise", "Em Desenvolvimento", "Concluído"],
                key="status",
                index=0 if not self._data.get("status") else None,
                help="Status atual do processo"
            )
    
    def _render_details(self) -> None:
        """Renderiza seção de detalhes."""
        st.text_area(
            "Descrição",
            key="description",
            value=self._data.get("description", ""),
            help="Descrição detalhada do processo"
        )
        
        st.text_area(
            "Objetivos",
            key="objectives",
            value=self._data.get("objectives", ""),
            help="Objetivos da automação"
        )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar", use_container_width=True):
                self._save_form()
        
        with col2:
            if st.button("🔄 Limpar", use_container_width=True):
                self._clear_form()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self._cancel_form()
    
    def _save_form(self) -> None:
        """Salva os dados do formulário."""
        try:
            # Coleta dados dos campos
            form_data = {
                "process_name": st.session_state.get("process_name", ""),
                "process_owner": st.session_state.get("process_owner", ""),
                "department": st.session_state.get("department", ""),
                "status": st.session_state.get("status", ""),
                "description": st.session_state.get("description", ""),
                "objectives": st.session_state.get("objectives", "")
            }
            
            # Valida dados
            if not form_data["process_name"]:
                st.error("Nome do processo é obrigatório")
                return
            
            # Tenta salvar
            if self.controller.create_process(form_data):
                st.success("Processo salvo com sucesso!")
                self._clear_form()
            else:
                st.error("Erro ao salvar processo")
                
        except Exception as e:
            st.error(f"Erro ao salvar: {str(e)}")
    
    def _clear_form(self) -> None:
        """Limpa os campos do formulário."""
        for key in [
            "process_name", "process_owner", "department",
            "status", "description", "objectives"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        self._data = {}
        st.rerun()
    
    def _cancel_form(self) -> None:
        """Cancela a edição do formulário."""
        self._clear_form()
        st.warning("Edição cancelada")

# Exporta a classe
__all__ = ['ProcessForm']