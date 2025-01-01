"""Formulário de sistemas envolvidos."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class SystemsForm:
    """Formulário de sistemas envolvidos."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "systems"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa lista de sistemas se necessário
        if "systems_list" not in st.session_state:
            st.session_state.systems_list = self.form_data.data.get("systems", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        systems = data.get("systems", [])
        
        if not systems:
            st.error("Adicione pelo menos um sistema")
            return False
        
        for system in systems:
            if not system.get("name"):
                st.error("Todos os sistemas precisam ter um nome")
                return False
            if not system.get("role"):
                st.error("Todos os sistemas precisam ter um papel definido")
                return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "systems": st.session_state.systems_list,
            "integrations": st.session_state.get("integrations", ""),
            "credentials": st.session_state.get("credentials", ""),
            "access_requirements": st.session_state.get("access_requirements", ""),
            "technical_constraints": st.session_state.get("technical_constraints", "")
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
    
    def _add_system(self, name: str, role: str, type: str, version: str) -> None:
        """
        Adiciona um novo sistema à lista.
        
        Args:
            name: Nome do sistema
            role: Papel no processo
            type: Tipo do sistema
            version: Versão do sistema
        """
        if not name:
            st.error("Nome do sistema é obrigatório")
            return
            
        if not role:
            st.error("Papel do sistema é obrigatório")
            return
        
        new_system = {
            "name": name,
            "role": role,
            "type": type,
            "version": version
        }
        
        st.session_state.systems_list.append(new_system)
        st.session_state.new_system_name = ""
        st.session_state.new_system_role = ""
        st.session_state.new_system_type = ""
        st.session_state.new_system_version = ""
    
    def _remove_system(self, index: int) -> None:
        """
        Remove um sistema da lista.
        
        Args:
            index: Índice do sistema a ser removido
        """
        st.session_state.systems_list.pop(index)
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 💻 Sistemas Envolvidos")
        
        # Adicionar novo sistema
        st.write("#### Adicionar Novo Sistema")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Nome do Sistema",
                key="new_system_name",
                help="Nome do sistema envolvido"
            )
            
            role = st.text_area(
                "Papel no Processo",
                key="new_system_role",
                help="Descreva o papel deste sistema no processo"
            )
        
        with col2:
            type = st.selectbox(
                "Tipo",
                options=[
                    "ERP", "CRM", "BPM", "ECM", "DMS",
                    "Legado", "Web", "Desktop", "Mobile", "Outro"
                ],
                key="new_system_type",
                help="Tipo do sistema"
            )
            
            version = st.text_input(
                "Versão",
                key="new_system_version",
                help="Versão do sistema"
            )
        
        if st.button("➕ Adicionar Sistema", use_container_width=True):
            self._add_system(name, role, type, version)
            st.rerun()
        
        # Lista de sistemas
        st.write("#### Sistemas Cadastrados")
        for i, system in enumerate(st.session_state.systems_list):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{system['name']}** ({system['type']} {system['version']})")
                    st.write(system['role'])
                
                with col2:
                    if st.button("🗑️", key=f"del_system_{i}"):
                        self._remove_system(i)
                        st.rerun()
                
                st.divider()
        
        # Informações adicionais
        st.text_area(
            "Integrações",
            key="integrations",
            value=self.form_data.data.get("integrations", ""),
            help="Descreva as integrações necessárias entre os sistemas"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Credenciais",
                key="credentials",
                value=self.form_data.data.get("credentials", ""),
                help="Liste as credenciais necessárias"
            )
            
            st.text_area(
                "Requisitos de Acesso",
                key="access_requirements",
                value=self.form_data.data.get("access_requirements", ""),
                help="Descreva os requisitos de acesso"
            )
        
        with col2:
            st.text_area(
                "Restrições Técnicas",
                key="technical_constraints",
                value=self.form_data.data.get("technical_constraints", ""),
                help="Liste as restrições técnicas"
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
                st.session_state.systems_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.systems_list = []
                st.warning("Edição cancelada")
                st.rerun() 