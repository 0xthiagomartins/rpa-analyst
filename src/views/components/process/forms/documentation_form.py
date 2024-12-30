"""Módulo do formulário de documentação."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class DocumentationForm(FormBase):
    """Formulário para documentação e anexos do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "documentation")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_document(self, documents: List[Dict[str, Any]]) -> None:
        """Adiciona um novo documento."""
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input(
                "Título",
                key="new_doc_title",
                help="Título do documento"
            )
            doc_type = st.selectbox(
                "Tipo",
                options=["Manual", "Tutorial", "Fluxograma", "Política", "Procedimento", "Outro"],
                key="new_doc_type"
            )
        with col2:
            version = st.text_input(
                "Versão",
                key="new_doc_version",
                help="Versão do documento"
            )
            status = st.selectbox(
                "Status",
                options=["Em Elaboração", "Em Revisão", "Aprovado", "Obsoleto"],
                key="new_doc_status"
            )
            
        description = st.text_area(
            "Descrição",
            key="new_doc_description",
            help="Descrição do documento"
        )
        
        # TODO: Implementar upload de arquivo quando disponível
        # file = st.file_uploader("Arquivo", key="new_doc_file")
            
        if st.button("➕ Adicionar Documento") and title and description:
            documents.append({
                "title": title,
                "type": doc_type,
                "version": version,
                "status": status,
                "description": description,
                # "file": file.name if file else None
            })
    
    def _add_reference(self, references: List[Dict[str, str]]) -> None:
        """Adiciona uma nova referência."""
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input(
                "Título",
                key="new_ref_title",
                help="Título da referência"
            )
        with col2:
            ref_type = st.selectbox(
                "Tipo",
                options=["Link", "Documento", "Artigo", "Norma", "Outro"],
                key="new_ref_type"
            )
            
        url = st.text_input(
            "URL/Localização",
            key="new_ref_url",
            help="URL ou localização da referência"
        )
            
        if st.button("➕ Adicionar Referência") and title and url:
            references.append({
                "title": title,
                "type": ref_type,
                "url": url
            })
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 📚 Documentação e Referências")
        
        # Inicializa listas se não existirem
        if "documents" not in self._data:
            self._data["documents"] = []
        if "references" not in self._data:
            self._data["references"] = []
            
        # Seção de Documentos
        st.write("#### Documentos")
        documents = self._data["documents"]
        
        # Lista documentos existentes
        for i, doc in enumerate(documents):
            with st.expander(f"{doc['type']}: {doc['title']} (v{doc['version']})"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    documents[i]["title"] = st.text_input(
                        "Título",
                        value=doc["title"],
                        key=f"doc_title_{i}"
                    )
                    col_type, col_version, col_status = st.columns(3)
                    with col_type:
                        documents[i]["type"] = st.selectbox(
                            "Tipo",
                            options=["Manual", "Tutorial", "Fluxograma", "Política", "Procedimento", "Outro"],
                            index=["Manual", "Tutorial", "Fluxograma", "Política", "Procedimento", "Outro"].index(doc["type"]),
                            key=f"doc_type_{i}"
                        )
                    with col_version:
                        documents[i]["version"] = st.text_input(
                            "Versão",
                            value=doc["version"],
                            key=f"doc_version_{i}"
                        )
                    with col_status:
                        documents[i]["status"] = st.selectbox(
                            "Status",
                            options=["Em Elaboração", "Em Revisão", "Aprovado", "Obsoleto"],
                            index=["Em Elaboração", "Em Revisão", "Aprovado", "Obsoleto"].index(doc["status"]),
                            key=f"doc_status_{i}"
                        )
                    documents[i]["description"] = st.text_area(
                        "Descrição",
                        value=doc["description"],
                        key=f"doc_description_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_doc_{i}"):
                        documents.pop(i)
                        st.rerun()
        
        # Adicionar novo documento
        self._add_document(documents)
        
        # Seção de Referências
        st.write("#### Referências")
        references = self._data["references"]
        
        # Lista referências existentes
        for i, ref in enumerate(references):
            with st.expander(f"{ref['type']}: {ref['title']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    references[i]["title"] = st.text_input(
                        "Título",
                        value=ref["title"],
                        key=f"ref_title_{i}"
                    )
                    references[i]["type"] = st.selectbox(
                        "Tipo",
                        options=["Link", "Documento", "Artigo", "Norma", "Outro"],
                        index=["Link", "Documento", "Artigo", "Norma", "Outro"].index(ref["type"]),
                        key=f"ref_type_{i}"
                    )
                    references[i]["url"] = st.text_input(
                        "URL/Localização",
                        value=ref["url"],
                        key=f"ref_url_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_ref_{i}"):
                        references.pop(i)
                        st.rerun()
        
        # Adicionar nova referência
        self._add_reference(references) 