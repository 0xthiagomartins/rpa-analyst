"""Módulo do formulário de passos do processo."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class StepsForm(FormBase):
    """Formulário para passos do processo (as-is e to-be)."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "steps")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_step(self, steps: List[Dict[str, str]], prefix: str) -> None:
        """Adiciona um novo passo."""
        col1, col2 = st.columns([3, 1])
        with col1:
            description = st.text_area(
                "Descrição do Passo",
                key=f"new_{prefix}_step_description",
                help="Descreva o passo do processo"
            )
        with col2:
            sequence = st.number_input(
                "Sequência",
                min_value=1,
                value=len(steps) + 1,
                key=f"new_{prefix}_step_sequence"
            )
            
        col1, col2 = st.columns(2)
        with col1:
            actor = st.text_input(
                "Responsável",
                key=f"new_{prefix}_step_actor",
                help="Quem executa este passo"
            )
        with col2:
            system = st.text_input(
                "Sistema",
                key=f"new_{prefix}_step_system",
                help="Sistema utilizado neste passo"
            )
            
        if st.button("➕ Adicionar Passo") and description:
            steps.append({
                "sequence": sequence,
                "description": description,
                "actor": actor,
                "system": system
            })
            steps.sort(key=lambda x: x["sequence"])
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 👣 Passos do Processo")
        
        # Inicializa listas se não existirem
        if "steps_as_is" not in self._data:
            self._data["steps_as_is"] = []
        if "steps_to_be" not in self._data:
            self._data["steps_to_be"] = []
            
        # Seção As-Is
        st.write("#### Processo Atual (As-Is)")
        steps_as_is = self._data["steps_as_is"]
        
        # Lista passos existentes
        for i, step in enumerate(steps_as_is):
            with st.expander(f"Passo {step['sequence']}: {step['description'][:50]}..."):
                col1, col2 = st.columns([4, 1])
                with col1:
                    steps_as_is[i]["sequence"] = st.number_input(
                        "Sequência",
                        min_value=1,
                        value=step["sequence"],
                        key=f"as_is_sequence_{i}"
                    )
                    steps_as_is[i]["description"] = st.text_area(
                        "Descrição",
                        value=step["description"],
                        key=f"as_is_description_{i}"
                    )
                    steps_as_is[i]["actor"] = st.text_input(
                        "Responsável",
                        value=step["actor"],
                        key=f"as_is_actor_{i}"
                    )
                    steps_as_is[i]["system"] = st.text_input(
                        "Sistema",
                        value=step["system"],
                        key=f"as_is_system_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_as_is_{i}"):
                        steps_as_is.pop(i)
                        st.rerun()
        
        # Adicionar novo passo as-is
        self._add_step(steps_as_is, "as_is")
        
        # Seção To-Be
        st.write("#### Processo Futuro (To-Be)")
        steps_to_be = self._data["steps_to_be"]
        
        # Lista passos existentes
        for i, step in enumerate(steps_to_be):
            with st.expander(f"Passo {step['sequence']}: {step['description'][:50]}..."):
                col1, col2 = st.columns([4, 1])
                with col1:
                    steps_to_be[i]["sequence"] = st.number_input(
                        "Sequência",
                        min_value=1,
                        value=step["sequence"],
                        key=f"to_be_sequence_{i}"
                    )
                    steps_to_be[i]["description"] = st.text_area(
                        "Descrição",
                        value=step["description"],
                        key=f"to_be_description_{i}"
                    )
                    steps_to_be[i]["actor"] = st.text_input(
                        "Responsável",
                        value=step["actor"],
                        key=f"to_be_actor_{i}"
                    )
                    steps_to_be[i]["system"] = st.text_input(
                        "Sistema",
                        value=step["system"],
                        key=f"to_be_system_{i}"
                    )
                with col2:
                    if st.button("🗑️", key=f"del_to_be_{i}"):
                        steps_to_be.pop(i)
                        st.rerun()
        
        # Adicionar novo passo to-be
        self._add_step(steps_to_be, "to_be") 