"""Formulário de sistemas e integrações."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from ..form_base import BaseForm
from ..form_field import FormField

class SystemsForm(BaseForm):
    """Formulário para sistemas e integrações."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("systems", container)
        
        # Inicializa campos
        self.systems_field = FormField(self.form_id, "systems")
        self.integrations_field = FormField(self.form_id, "integrations")
        self.credentials_field = FormField(self.form_id, "credentials")
        
        # Inicializa listas se não existirem
        if "systems_list" not in st.session_state:
            st.session_state.systems_list = self.form_data.data.get("systems", [])
        if "integrations_list" not in st.session_state:
            st.session_state.integrations_list = self.form_data.data.get("integrations", [])
        if "credentials_list" not in st.session_state:
            st.session_state.credentials_list = self.form_data.data.get("credentials", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida sistemas
        if not st.session_state.systems_list:
            errors.append("Pelo menos um sistema é obrigatório")
            is_valid = False
        
        # Valida credenciais para cada sistema
        systems_with_credentials = {cred["system"] for cred in st.session_state.credentials_list}
        systems_without_credentials = [
            sys["name"] for sys in st.session_state.systems_list 
            if sys["name"] not in systems_with_credentials
        ]
        
        if systems_without_credentials:
            errors.append(
                "Os seguintes sistemas não possuem credenciais cadastradas: " +
                ", ".join(systems_without_credentials)
            )
            is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_system(self) -> None:
        """Adiciona um novo sistema."""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nome do Sistema", key="new_system_name")
        with col2:
            role = st.text_input("Função no Processo", key="new_system_role")
            
        if st.button("➕ Adicionar Sistema"):
            if name and role:
                new_system = {"name": name, "role": role}
                st.session_state.systems_list.append(new_system)
                self.update_field("systems", st.session_state.systems_list)
                st.rerun()
            else:
                st.error("Preencha o nome e a função do sistema")
    
    def _add_integration(self) -> None:
        """Adiciona uma nova integração."""
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_input("Sistema Origem", key="new_integration_source")
        with col2:
            target = st.text_input("Sistema Destino", key="new_integration_target")
            
        description = st.text_area("Descrição da Integração", key="new_integration_desc")
            
        if st.button("➕ Adicionar Integração"):
            if source and target and description:
                new_integration = {
                    "source": source,
                    "target": target,
                    "description": description
                }
                st.session_state.integrations_list.append(new_integration)
                self.update_field("integrations", st.session_state.integrations_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos da integração")
    
    def _add_credential(self) -> None:
        """Adiciona uma nova credencial."""
        col1, col2 = st.columns(2)
        with col1:
            system = st.text_input("Sistema", key="new_credential_system")
        with col2:
            access_type = st.selectbox(
                "Tipo de Acesso",
                options=["Usuário/Senha", "API Key", "Token", "Certificado", "Outro"],
                key="new_credential_type"
            )
            
        notes = st.text_area("Observações", key="new_credential_notes")
            
        if st.button("➕ Adicionar Credencial"):
            if system and access_type:
                new_credential = {
                    "system": system,
                    "access_type": access_type,
                    "notes": notes
                }
                st.session_state.credentials_list.append(new_credential)
                self.update_field("credentials", st.session_state.credentials_list)
                st.rerun()
            else:
                st.error("Preencha o sistema e o tipo de acesso")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("💻 Sistemas e Integrações")
        
        # Seção de Sistemas
        st.write("#### Sistemas")
        
        # Lista sistemas existentes
        for i, system in enumerate(st.session_state.systems_list):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_name = st.text_input(
                    "Nome",
                    value=system["name"],
                    key=f"system_name_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_role = st.text_input(
                    "Função",
                    value=system["role"],
                    key=f"system_role_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_system_{i}"):
                    st.session_state.systems_list.pop(i)
                    self.update_field("systems", st.session_state.systems_list)
                    st.rerun()
            
            if self.is_editing and (new_name != system["name"] or new_role != system["role"]):
                st.session_state.systems_list[i] = {
                    "name": new_name,
                    "role": new_role
                }
                self.update_field("systems", st.session_state.systems_list)
        
        # Adicionar novo sistema
        if self.is_editing:
            self._add_system()
        
        # Seção de Integrações
        st.write("#### Integrações")
        
        # Lista integrações existentes
        for i, integration in enumerate(st.session_state.integrations_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_source = st.text_input(
                    "Origem",
                    value=integration["source"],
                    key=f"integration_source_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_target = st.text_input(
                    "Destino",
                    value=integration["target"],
                    key=f"integration_target_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_integration_{i}"):
                    st.session_state.integrations_list.pop(i)
                    self.update_field("integrations", st.session_state.integrations_list)
                    st.rerun()
            
            new_description = st.text_area(
                "Descrição",
                value=integration["description"],
                key=f"integration_desc_{i}",
                disabled=not self.is_editing
            )
            
            if self.is_editing and (
                new_source != integration["source"] or 
                new_target != integration["target"] or
                new_description != integration["description"]
            ):
                st.session_state.integrations_list[i] = {
                    "source": new_source,
                    "target": new_target,
                    "description": new_description
                }
                self.update_field("integrations", st.session_state.integrations_list)
        
        # Adicionar nova integração
        if self.is_editing:
            self._add_integration()
        
        # Seção de Credenciais
        st.write("#### Credenciais")
        
        # Lista credenciais existentes
        for i, credential in enumerate(st.session_state.credentials_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_system = st.text_input(
                    "Sistema",
                    value=credential["system"],
                    key=f"credential_system_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_type = st.selectbox(
                    "Tipo",
                    options=["Usuário/Senha", "API Key", "Token", "Certificado", "Outro"],
                    index=["Usuário/Senha", "API Key", "Token", "Certificado", "Outro"].index(credential["access_type"]),
                    key=f"credential_type_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_credential_{i}"):
                    st.session_state.credentials_list.pop(i)
                    self.update_field("credentials", st.session_state.credentials_list)
                    st.rerun()
            
            new_notes = st.text_area(
                "Observações",
                value=credential["notes"],
                key=f"credential_notes_{i}",
                disabled=not self.is_editing
            )
            
            if self.is_editing and (
                new_system != credential["system"] or 
                new_type != credential["access_type"] or
                new_notes != credential["notes"]
            ):
                st.session_state.credentials_list[i] = {
                    "system": new_system,
                    "access_type": new_type,
                    "notes": new_notes
                }
                self.update_field("credentials", st.session_state.credentials_list)
        
        # Adicionar nova credencial
        if self.is_editing:
            self._add_credential() 