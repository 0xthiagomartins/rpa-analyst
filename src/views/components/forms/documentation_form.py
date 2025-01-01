"""Formulário de documentação do processo."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class DocumentationForm:
    """Formulário de documentação do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "documentation"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa listas se necessário
        if "attachments_list" not in st.session_state:
            st.session_state.attachments_list = self.form_data.data.get("attachments", [])
        if "references_list" not in st.session_state:
            st.session_state.references_list = self.form_data.data.get("references", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        
        if not data.get("process_summary"):
            st.error("O resumo do processo é obrigatório")
            return False
            
        if not data.get("implementation_notes"):
            st.error("As notas de implementação são obrigatórias")
            return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "process_summary": st.session_state.get("process_summary", ""),
            "implementation_notes": st.session_state.get("implementation_notes", ""),
            "assumptions": st.session_state.get("assumptions", ""),
            "limitations": st.session_state.get("limitations", ""),
            "attachments": st.session_state.attachments_list,
            "references": st.session_state.references_list,
            "additional_notes": st.session_state.get("additional_notes", ""),
            "review_notes": st.session_state.get("review_notes", "")
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
    
    def _add_attachment(self, name: str, description: str, file_type: str) -> None:
        """
        Adiciona um novo anexo à lista.
        
        Args:
            name: Nome do anexo
            description: Descrição do anexo
            file_type: Tipo do arquivo
        """
        if not name:
            st.error("Nome do anexo é obrigatório")
            return
        
        new_attachment = {
            "name": name,
            "description": description,
            "type": file_type
        }
        
        st.session_state.attachments_list.append(new_attachment)
        st.session_state.new_attachment_name = ""
        st.session_state.new_attachment_description = ""
        st.session_state.new_attachment_type = ""
    
    def _remove_attachment(self, index: int) -> None:
        """
        Remove um anexo da lista.
        
        Args:
            index: Índice do anexo a ser removido
        """
        st.session_state.attachments_list.pop(index)
    
    def _add_reference(self, title: str, link: str, description: str) -> None:
        """
        Adiciona uma nova referência à lista.
        
        Args:
            title: Título da referência
            link: Link da referência
            description: Descrição da referência
        """
        if not title:
            st.error("Título da referência é obrigatório")
            return
        
        new_reference = {
            "title": title,
            "link": link,
            "description": description
        }
        
        st.session_state.references_list.append(new_reference)
        st.session_state.new_reference_title = ""
        st.session_state.new_reference_link = ""
        st.session_state.new_reference_description = ""
    
    def _remove_reference(self, index: int) -> None:
        """
        Remove uma referência da lista.
        
        Args:
            index: Índice da referência a ser removida
        """
        st.session_state.references_list.pop(index)
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📄 Documentação do Processo")
        
        # Resumo e notas principais
        st.text_area(
            "Resumo do Processo",
            key="process_summary",
            value=self.form_data.data.get("process_summary", ""),
            help="Resumo geral do processo e seus objetivos",
            height=150
        )
        
        st.text_area(
            "Notas de Implementação",
            key="implementation_notes",
            value=self.form_data.data.get("implementation_notes", ""),
            help="Notas importantes para a implementação",
            height=150
        )
        
        # Premissas e limitações
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Premissas",
                key="assumptions",
                value=self.form_data.data.get("assumptions", ""),
                help="Premissas consideradas"
            )
        
        with col2:
            st.text_area(
                "Limitações",
                key="limitations",
                value=self.form_data.data.get("limitations", ""),
                help="Limitações identificadas"
            )
        
        # Anexos
        st.write("#### 📎 Anexos")
        
        # Adicionar novo anexo
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            attachment_name = st.text_input(
                "Nome do Anexo",
                key="new_attachment_name",
                help="Nome do arquivo anexo"
            )
        
        with col2:
            attachment_description = st.text_input(
                "Descrição",
                key="new_attachment_description",
                help="Descrição do anexo"
            )
        
        with col3:
            file_type = st.selectbox(
                "Tipo",
                options=["Documento", "Planilha", "Imagem", "Outro"],
                key="new_attachment_type",
                help="Tipo do arquivo"
            )
        
        if st.button("➕ Adicionar Anexo", key="add_attachment", use_container_width=True):
            self._add_attachment(attachment_name, attachment_description, file_type)
            st.rerun()
        
        # Lista de anexos
        for i, attachment in enumerate(st.session_state.attachments_list):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{attachment['name']}** ({attachment['type']})")
                    if attachment.get('description'):
                        st.write(attachment['description'])
                
                with col2:
                    if st.button("🗑️", key=f"del_attachment_{i}"):
                        self._remove_attachment(i)
                        st.rerun()
                
                st.divider()
        
        # Referências
        st.write("#### 🔗 Referências")
        
        # Adicionar nova referência
        col1, col2 = st.columns(2)
        
        with col1:
            reference_title = st.text_input(
                "Título",
                key="new_reference_title",
                help="Título da referência"
            )
            
            reference_link = st.text_input(
                "Link",
                key="new_reference_link",
                help="Link para a referência"
            )
        
        with col2:
            reference_description = st.text_area(
                "Descrição",
                key="new_reference_description",
                help="Descrição da referência"
            )
        
        if st.button("➕ Adicionar Referência", key="add_reference", use_container_width=True):
            self._add_reference(reference_title, reference_link, reference_description)
            st.rerun()
        
        # Lista de referências
        for i, reference in enumerate(st.session_state.references_list):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if reference.get('link'):
                        st.markdown(f"**[{reference['title']}]({reference['link']})**")
                    else:
                        st.write(f"**{reference['title']}**")
                    
                    if reference.get('description'):
                        st.write(reference['description'])
                
                with col2:
                    if st.button("🗑️", key=f"del_reference_{i}"):
                        self._remove_reference(i)
                        st.rerun()
                
                st.divider()
        
        # Notas adicionais
        st.write("#### 📝 Notas Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Notas Adicionais",
                key="additional_notes",
                value=self.form_data.data.get("additional_notes", ""),
                help="Outras informações relevantes"
            )
        
        with col2:
            st.text_area(
                "Notas de Revisão",
                key="review_notes",
                value=self.form_data.data.get("review_notes", ""),
                help="Notas da revisão do processo"
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
                st.session_state.attachments_list = []
                st.session_state.references_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.attachments_list = []
                st.session_state.references_list = []
                st.warning("Edição cancelada")
                st.rerun() 