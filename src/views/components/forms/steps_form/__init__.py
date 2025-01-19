"""Formulário de passos do processo."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from ..form_base import BaseForm
from ..form_field import FormField

class StepsForm(BaseForm):
    """Formulário para passos do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("steps", container)
        
        # Inicializa campos
        self.steps_field = FormField(self.form_id, "steps")
        self.decisions_field = FormField(self.form_id, "decisions")
        self.loops_field = FormField(self.form_id, "loops")
        
        # Inicializa listas se não existirem
        if "steps_list" not in st.session_state:
            st.session_state.steps_list = self.form_data.data.get("steps", [])
        if "decisions_list" not in st.session_state:
            st.session_state.decisions_list = self.form_data.data.get("decisions", [])
        if "loops_list" not in st.session_state:
            st.session_state.loops_list = self.form_data.data.get("loops", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida passos
        if not st.session_state.steps_list:
            errors.append("Pelo menos um passo é obrigatório")
            is_valid = False
        
        # Valida sequência dos passos
        step_sequences = [step["sequence"] for step in st.session_state.steps_list]
        if len(set(step_sequences)) != len(step_sequences):
            errors.append("Existem passos com a mesma sequência")
            is_valid = False
        
        # Valida decisões
        for decision in st.session_state.decisions_list:
            step = decision["step"]
            if step not in step_sequences:
                errors.append(f"Decisão referencia passo inexistente: {step}")
                is_valid = False
        
        # Valida loops
        for loop in st.session_state.loops_list:
            start = loop["start_step"]
            end = loop["end_step"]
            if start not in step_sequences or end not in step_sequences:
                errors.append(f"Loop referencia passo inexistente: {start} -> {end}")
                is_valid = False
            if start >= end:
                errors.append(f"Loop inválido: início ({start}) deve ser menor que fim ({end})")
                is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_step(self) -> None:
        """Adiciona um novo passo."""
        col1, col2 = st.columns(2)
        with col1:
            sequence = st.number_input("Sequência", min_value=1, key="new_step_seq")
        with col2:
            actor = st.text_input("Responsável", key="new_step_actor")
            
        description = st.text_area(
            "Descrição do Passo",
            key="new_step_desc",
            help="Descreva a ação a ser executada"
        )
            
        if st.button("➕ Adicionar Passo"):
            if sequence and actor and description:
                new_step = {
                    "sequence": sequence,
                    "actor": actor,
                    "description": description
                }
                st.session_state.steps_list.append(new_step)
                # Ordena por sequência
                st.session_state.steps_list.sort(key=lambda x: x["sequence"])
                self.update_field("steps", st.session_state.steps_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_decision(self) -> None:
        """Adiciona um novo ponto de decisão."""
        step = st.number_input("Passo", min_value=1, key="new_decision_step")
        condition = st.text_area(
            "Condição",
            key="new_decision_condition",
            help="Ex: Se valor > 1000"
        )
        true_path = st.text_area("Caminho Verdadeiro", key="new_decision_true")
        false_path = st.text_area("Caminho Falso", key="new_decision_false")
            
        if st.button("➕ Adicionar Decisão"):
            if step and condition and true_path and false_path:
                new_decision = {
                    "step": step,
                    "condition": condition,
                    "true_path": true_path,
                    "false_path": false_path
                }
                st.session_state.decisions_list.append(new_decision)
                self.update_field("decisions", st.session_state.decisions_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_loop(self) -> None:
        """Adiciona um novo loop."""
        start_step = st.number_input("Passo Inicial", min_value=1, key="new_loop_start")
        end_step = st.number_input("Passo Final", min_value=1, key="new_loop_end")
        condition = st.text_area(
            "Condição de Parada",
            key="new_loop_condition",
            help="Ex: Até processar todos os registros"
        )
            
        if st.button("➕ Adicionar Loop"):
            if start_step and end_step and condition:
                new_loop = {
                    "start_step": start_step,
                    "end_step": end_step,
                    "condition": condition
                }
                st.session_state.loops_list.append(new_loop)
                self.update_field("loops", st.session_state.loops_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("👣 Passos do Processo")
        
        # Seção de Passos
        st.write("#### Passos")
        
        # Lista passos existentes
        for i, step in enumerate(st.session_state.steps_list):
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                new_sequence = st.number_input(
                    "Seq.",
                    value=step["sequence"],
                    min_value=1,
                    key=f"step_seq_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_actor = st.text_input(
                    "Responsável",
                    value=step["actor"],
                    key=f"step_actor_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                new_description = st.text_area(
                    "Descrição",
                    value=step["description"],
                    key=f"step_desc_{i}",
                    disabled=not self.is_editing
                )
            with col4:
                if self.is_editing and st.button("🗑️", key=f"del_step_{i}"):
                    st.session_state.steps_list.pop(i)
                    self.update_field("steps", st.session_state.steps_list)
                    st.rerun()
            
            if self.is_editing and (
                new_sequence != step["sequence"] or
                new_actor != step["actor"] or
                new_description != step["description"]
            ):
                st.session_state.steps_list[i] = {
                    "sequence": new_sequence,
                    "actor": new_actor,
                    "description": new_description
                }
                # Reordena por sequência
                st.session_state.steps_list.sort(key=lambda x: x["sequence"])
                self.update_field("steps", st.session_state.steps_list)
        
        # Adicionar novo passo
        if self.is_editing:
            self._add_step()
        
        # Seção de Decisões
        st.write("#### Pontos de Decisão")
        
        # Lista decisões existentes
        for i, decision in enumerate(st.session_state.decisions_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                new_step = st.number_input(
                    "Passo",
                    value=decision["step"],
                    min_value=1,
                    key=f"decision_step_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_condition = st.text_area(
                    "Condição",
                    value=decision["condition"],
                    key=f"decision_condition_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_decision_{i}"):
                    st.session_state.decisions_list.pop(i)
                    self.update_field("decisions", st.session_state.decisions_list)
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                new_true_path = st.text_area(
                    "Se Verdadeiro",
                    value=decision["true_path"],
                    key=f"decision_true_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_false_path = st.text_area(
                    "Se Falso",
                    value=decision["false_path"],
                    key=f"decision_false_{i}",
                    disabled=not self.is_editing
                )
            
            if self.is_editing and (
                new_step != decision["step"] or
                new_condition != decision["condition"] or
                new_true_path != decision["true_path"] or
                new_false_path != decision["false_path"]
            ):
                st.session_state.decisions_list[i] = {
                    "step": new_step,
                    "condition": new_condition,
                    "true_path": new_true_path,
                    "false_path": new_false_path
                }
                self.update_field("decisions", st.session_state.decisions_list)
        
        # Adicionar nova decisão
        if self.is_editing:
            self._add_decision()
        
        # Seção de Loops
        st.write("#### Loops")
        
        # Lista loops existentes
        for i, loop in enumerate(st.session_state.loops_list):
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
            with col1:
                new_start = st.number_input(
                    "Início",
                    value=loop["start_step"],
                    min_value=1,
                    key=f"loop_start_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_end = st.number_input(
                    "Fim",
                    value=loop["end_step"],
                    min_value=1,
                    key=f"loop_end_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                new_condition = st.text_area(
                    "Condição",
                    value=loop["condition"],
                    key=f"loop_condition_{i}",
                    disabled=not self.is_editing
                )
            with col4:
                if self.is_editing and st.button("🗑️", key=f"del_loop_{i}"):
                    st.session_state.loops_list.pop(i)
                    self.update_field("loops", st.session_state.loops_list)
                    st.rerun()
            
            if self.is_editing and (
                new_start != loop["start_step"] or
                new_end != loop["end_step"] or
                new_condition != loop["condition"]
            ):
                st.session_state.loops_list[i] = {
                    "start_step": new_start,
                    "end_step": new_end,
                    "condition": new_condition
                }
                self.update_field("loops", st.session_state.loops_list)
        
        # Adicionar novo loop
        if self.is_editing:
            self._add_loop() 