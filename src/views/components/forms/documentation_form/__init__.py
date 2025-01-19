"""Formulário de documentação do processo."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from ..form_base import BaseForm
from ..form_field import FormField

class DocumentationForm(BaseForm):
    """Formulário para documentação do processo."""
    
    DOC_TYPES = [
        "Manual", "Procedimento", "Instrução de Trabalho", 
        "Fluxograma", "Política", "Formulário", "Outro"
    ]
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("documentation", container)
        
        # Inicializa campos
        self.docs_field = FormField(self.form_id, "documents")
        self.references_field = FormField(self.form_id, "references")
        self.notes_field = FormField(self.form_id, "notes")
        
        # Inicializa listas se não existirem
        if "docs_list" not in st.session_state:
            st.session_state.docs_list = self.form_data.data.get("documents", [])
        if "references_list" not in st.session_state:
            st.session_state.references_list = self.form_data.data.get("references", [])
        if "notes_list" not in st.session_state:
            st.session_state.notes_list = self.form_data.data.get("notes", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida documentos
        if not st.session_state.docs_list:
            errors.append("Pelo menos um documento deve ser registrado")
            is_valid = False
        
        # Valida campos obrigatórios dos documentos
        for doc in st.session_state.docs_list:
            if not doc.get("title") or not doc.get("description"):
                errors.append(f"O documento '{doc.get('type')}' precisa ter título e descrição")
                is_valid = False
            if not doc.get("location"):
                errors.append(f"O documento '{doc.get('title')}' precisa ter localização/link")
                is_valid = False
        
        # Valida campos obrigatórios das referências
        for ref in st.session_state.references_list:
            if not ref.get("title") or not ref.get("description"):
                errors.append("Todas as referências precisam ter título e descrição")
                is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_document(self) -> None:
        """Adiciona um novo documento."""
        col1, col2 = st.columns(2)
        with col1:
            doc_type = st.selectbox(
                "Tipo de Documento",
                options=self.DOC_TYPES,
                key="new_doc_type"
            )
        with col2:
            title = st.text_input("Título", key="new_doc_title")
            
        description = st.text_area(
            "Descrição",
            key="new_doc_desc",
            help="Descreva o conteúdo e propósito do documento"
        )
        
        location = st.text_input(
            "Localização/Link",
            key="new_doc_location",
            help="Onde o documento pode ser encontrado"
        )
            
        if st.button("➕ Adicionar Documento"):
            if doc_type and title and description and location:
                new_doc = {
                    "type": doc_type,
                    "title": title,
                    "description": description,
                    "location": location
                }
                st.session_state.docs_list.append(new_doc)
                self.update_field("documents", st.session_state.docs_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_reference(self) -> None:
        """Adiciona uma nova referência."""
        title = st.text_input("Título da Referência", key="new_ref_title")
        description = st.text_area(
            "Descrição",
            key="new_ref_desc",
            help="Descreva como esta referência se relaciona com o processo"
        )
        link = st.text_input(
            "Link/Localização",
            key="new_ref_link"
        )
            
        if st.button("➕ Adicionar Referência"):
            if title and description:
                new_ref = {
                    "title": title,
                    "description": description,
                    "link": link
                }
                st.session_state.references_list.append(new_ref)
                self.update_field("references", st.session_state.references_list)
                st.rerun()
            else:
                st.error("Preencha título e descrição")
    
    def _add_note(self) -> None:
        """Adiciona uma nova nota."""
        note = st.text_area(
            "Nota",
            key="new_note",
            help="Adicione observações, comentários ou informações adicionais"
        )
            
        if st.button("➕ Adicionar Nota"):
            if note:
                st.session_state.notes_list.append(note)
                self.update_field("notes", st.session_state.notes_list)
                st.rerun()
            else:
                st.error("Digite a nota")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("📄 Documentação")
        
        # Seção de Documentos
        st.write("#### Documentos")
        
        # Lista documentos existentes
        for i, doc in enumerate(st.session_state.docs_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_type = st.selectbox(
                    "Tipo",
                    options=self.DOC_TYPES,
                    index=self.DOC_TYPES.index(doc["type"]),
                    key=f"doc_type_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_title = st.text_input(
                    "Título",
                    value=doc["title"],
                    key=f"doc_title_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_doc_{i}"):
                    st.session_state.docs_list.pop(i)
                    self.update_field("documents", st.session_state.docs_list)
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                new_description = st.text_area(
                    "Descrição",
                    value=doc["description"],
                    key=f"doc_desc_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_location = st.text_input(
                    "Localização/Link",
                    value=doc["location"],
                    key=f"doc_location_{i}",
                    disabled=not self.is_editing
                )
            
            if self.is_editing and (
                new_type != doc["type"] or
                new_title != doc["title"] or
                new_description != doc["description"] or
                new_location != doc["location"]
            ):
                st.session_state.docs_list[i] = {
                    "type": new_type,
                    "title": new_title,
                    "description": new_description,
                    "location": new_location
                }
                self.update_field("documents", st.session_state.docs_list)
        
        # Adicionar novo documento
        if self.is_editing:
            self._add_document()
        
        # Seção de Referências
        st.write("#### Referências")
        
        # Lista referências existentes
        for i, ref in enumerate(st.session_state.references_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_title = st.text_input(
                    "Título",
                    value=ref["title"],
                    key=f"ref_title_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_link = st.text_input(
                    "Link",
                    value=ref["link"],
                    key=f"ref_link_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_ref_{i}"):
                    st.session_state.references_list.pop(i)
                    self.update_field("references", st.session_state.references_list)
                    st.rerun()
            
            new_description = st.text_area(
                "Descrição",
                value=ref["description"],
                key=f"ref_desc_{i}",
                disabled=not self.is_editing
            )
            
            if self.is_editing and (
                new_title != ref["title"] or
                new_description != ref["description"] or
                new_link != ref["link"]
            ):
                st.session_state.references_list[i] = {
                    "title": new_title,
                    "description": new_description,
                    "link": new_link
                }
                self.update_field("references", st.session_state.references_list)
        
        # Adicionar nova referência
        if self.is_editing:
            self._add_reference()
        
        # Seção de Notas
        st.write("#### Notas e Observações")
        
        # Lista notas existentes
        for i, note in enumerate(st.session_state.notes_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_note = st.text_area(
                    f"Nota {i+1}",
                    value=note,
                    key=f"note_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                if self.is_editing and st.button("🗑️", key=f"del_note_{i}"):
                    st.session_state.notes_list.pop(i)
                    self.update_field("notes", st.session_state.notes_list)
                    st.rerun()
            
            if self.is_editing and new_note != note:
                st.session_state.notes_list[i] = new_note
                self.update_field("notes", st.session_state.notes_list)
        
        # Adicionar nova nota
        if self.is_editing:
            self._add_note() 