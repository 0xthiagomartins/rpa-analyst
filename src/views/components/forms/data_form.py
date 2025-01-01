"""Formulário de dados do processo."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class DataForm:
    """Formulário de dados do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "data"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa listas se necessário
        if "inputs_list" not in st.session_state:
            st.session_state.inputs_list = self.form_data.data.get("inputs", [])
        if "outputs_list" not in st.session_state:
            st.session_state.outputs_list = self.form_data.data.get("outputs", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        inputs = data.get("inputs", [])
        outputs = data.get("outputs", [])
        
        if not inputs:
            st.error("Adicione pelo menos uma entrada de dados")
            return False
        
        if not outputs:
            st.error("Adicione pelo menos uma saída de dados")
            return False
        
        for input_data in inputs:
            if not input_data.get("name"):
                st.error("Todas as entradas precisam ter um nome")
                return False
            if not input_data.get("type"):
                st.error("Todas as entradas precisam ter um tipo")
                return False
        
        for output_data in outputs:
            if not output_data.get("name"):
                st.error("Todas as saídas precisam ter um nome")
                return False
            if not output_data.get("type"):
                st.error("Todas as saídas precisam ter um tipo")
                return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "inputs": st.session_state.inputs_list,
            "outputs": st.session_state.outputs_list,
            "data_sources": st.session_state.get("data_sources", ""),
            "data_format": st.session_state.get("data_format", ""),
            "data_volume": st.session_state.get("data_volume", ""),
            "data_quality": st.session_state.get("data_quality", ""),
            "data_security": st.session_state.get("data_security", "")
        }
    
    def save(self) -> bool:
        """
        Salva os dados do formulário.
        
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        data = self.get_data()
        is_valid = self.validate()
        
        # Atualiza estado
        self.state_manager.update_form_data(
            self.form_id,
            data=data,
            is_valid=is_valid,
            state=FormState.COMPLETED if is_valid else FormState.INVALID
        )
        
        return is_valid
    
    def _add_data_item(self, name: str, type: str, description: str, is_input: bool) -> None:
        """
        Adiciona um item de dado à lista apropriada.
        
        Args:
            name: Nome do dado
            type: Tipo do dado
            description: Descrição do dado
            is_input: Se é entrada (True) ou saída (False)
        """
        if not name:
            st.error("Nome do dado é obrigatório")
            return
            
        if not type:
            st.error("Tipo do dado é obrigatório")
            return
        
        new_item = {
            "name": name,
            "type": type,
            "description": description
        }
        
        if is_input:
            st.session_state.inputs_list.append(new_item)
            st.session_state.new_input_name = ""
            st.session_state.new_input_type = ""
            st.session_state.new_input_description = ""
        else:
            st.session_state.outputs_list.append(new_item)
            st.session_state.new_output_name = ""
            st.session_state.new_output_type = ""
            st.session_state.new_output_description = ""
    
    def _remove_data_item(self, index: int, is_input: bool) -> None:
        """
        Remove um item de dado da lista apropriada.
        
        Args:
            index: Índice do item
            is_input: Se é entrada (True) ou saída (False)
        """
        if is_input:
            st.session_state.inputs_list.pop(index)
        else:
            st.session_state.outputs_list.pop(index)
    
    def _render_data_list(self, title: str, items: List[Dict[str, str]], is_input: bool) -> None:
        """
        Renderiza uma lista de dados.
        
        Args:
            title: Título da seção
            items: Lista de itens
            is_input: Se é entrada (True) ou saída (False)
        """
        st.write(f"#### {title}")
        
        # Adicionar novo item
        col1, col2, col3 = st.columns([2, 1, 2])
        
        prefix = "input" if is_input else "output"
        with col1:
            name = st.text_input(
                "Nome",
                key=f"new_{prefix}_name",
                help="Nome do dado"
            )
        
        with col2:
            type = st.selectbox(
                "Tipo",
                options=[
                    "Texto", "Número", "Data", "Booleano", 
                    "Lista", "Arquivo", "Imagem", "Outro"
                ],
                key=f"new_{prefix}_type",
                help="Tipo do dado"
            )
        
        with col3:
            description = st.text_input(
                "Descrição",
                key=f"new_{prefix}_description",
                help="Descrição do dado"
            )
        
        if st.button(f"➕ Adicionar {title}", key=f"add_{prefix}", use_container_width=True):
            self._add_data_item(name, type, description, is_input)
            st.rerun()
        
        # Lista de itens
        for i, item in enumerate(items):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{item['name']}** ({item['type']})")
                    if item.get('description'):
                        st.write(item['description'])
                
                with col2:
                    if st.button("🗑️", key=f"del_{prefix}_{i}"):
                        self._remove_data_item(i, is_input)
                        st.rerun()
                
                st.divider()
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📊 Dados do Processo")
        
        # Entradas e Saídas
        tab1, tab2 = st.tabs(["📥 Entradas", "📤 Saídas"])
        
        with tab1:
            self._render_data_list(
                "Dados de Entrada",
                st.session_state.inputs_list,
                True
            )
        
        with tab2:
            self._render_data_list(
                "Dados de Saída",
                st.session_state.outputs_list,
                False
            )
        
        # Informações adicionais
        st.write("#### Informações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Fontes de Dados",
                key="data_sources",
                value=self.form_data.data.get("data_sources", ""),
                help="Liste as fontes dos dados"
            )
            
            st.text_area(
                "Formato dos Dados",
                key="data_format",
                value=self.form_data.data.get("data_format", ""),
                help="Descreva o formato dos dados"
            )
            
            st.text_area(
                "Volume de Dados",
                key="data_volume",
                value=self.form_data.data.get("data_volume", ""),
                help="Estime o volume de dados"
            )
        
        with col2:
            st.text_area(
                "Qualidade dos Dados",
                key="data_quality",
                value=self.form_data.data.get("data_quality", ""),
                help="Avalie a qualidade dos dados"
            )
            
            st.text_area(
                "Segurança dos Dados",
                key="data_security",
                value=self.form_data.data.get("data_security", ""),
                help="Descreva requisitos de segurança"
            )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar", use_container_width=True):
                if self.save():
                    st.success("Dados salvos com sucesso!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Limpar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.inputs_list = []
                st.session_state.outputs_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.inputs_list = []
                st.session_state.outputs_list = []
                st.warning("Edição cancelada")
                st.rerun() 