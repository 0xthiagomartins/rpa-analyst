"""Formulário de passos do processo."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class StepsForm:
    """Formulário de passos do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "steps"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa lista de passos se necessário
        if "steps_list" not in st.session_state:
            st.session_state.steps_list = self.form_data.data.get("steps", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        steps = data.get("steps", [])
        
        if not steps:
            st.error("Adicione pelo menos um passo")
            return False
        
        for step in steps:
            if not step.get("description"):
                st.error("Todos os passos precisam ter uma descrição")
                return False
            if not step.get("type"):
                st.error("Todos os passos precisam ter um tipo")
                return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "steps": st.session_state.steps_list,
            "process_flow": st.session_state.get("process_flow", ""),
            "decision_points": st.session_state.get("decision_points", ""),
            "exceptions": st.session_state.get("exceptions", ""),
            "validations": st.session_state.get("validations", "")
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
    
    def _add_step(
        self, 
        description: str, 
        step_type: str, 
        actor: str,
        system: str,
        inputs: str,
        outputs: str
    ) -> None:
        """
        Adiciona um novo passo à lista.
        
        Args:
            description: Descrição do passo
            step_type: Tipo do passo
            actor: Responsável pelo passo
            system: Sistema envolvido
            inputs: Entradas necessárias
            outputs: Saídas geradas
        """
        if not description:
            st.error("Descrição do passo é obrigatória")
            return
            
        if not step_type:
            st.error("Tipo do passo é obrigatório")
            return
        
        new_step = {
            "description": description,
            "type": step_type,
            "actor": actor,
            "system": system,
            "inputs": inputs,
            "outputs": outputs,
            "order": len(st.session_state.steps_list) + 1
        }
        
        st.session_state.steps_list.append(new_step)
        st.session_state.new_step_description = ""
        st.session_state.new_step_type = ""
        st.session_state.new_step_actor = ""
        st.session_state.new_step_system = ""
        st.session_state.new_step_inputs = ""
        st.session_state.new_step_outputs = ""
    
    def _remove_step(self, index: int) -> None:
        """
        Remove um passo da lista.
        
        Args:
            index: Índice do passo a ser removido
        """
        st.session_state.steps_list.pop(index)
        
        # Reordena os passos restantes
        for i, step in enumerate(st.session_state.steps_list, 1):
            step["order"] = i
    
    def _move_step(self, index: int, direction: int) -> None:
        """
        Move um passo para cima ou para baixo.
        
        Args:
            index: Índice do passo
            direction: 1 para baixo, -1 para cima
        """
        new_index = index + direction
        if 0 <= new_index < len(st.session_state.steps_list):
            st.session_state.steps_list[index], st.session_state.steps_list[new_index] = \
                st.session_state.steps_list[new_index], st.session_state.steps_list[index]
            
            # Atualiza a ordem
            st.session_state.steps_list[index]["order"] = index + 1
            st.session_state.steps_list[new_index]["order"] = new_index + 1
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### 👣 Passos do Processo")
        
        # Adicionar novo passo
        st.write("#### Adicionar Novo Passo")
        
        # Descrição e tipo
        col1, col2 = st.columns([3, 1])
        
        with col1:
            description = st.text_area(
                "Descrição do Passo",
                key="new_step_description",
                help="Descreva o que deve ser feito"
            )
        
        with col2:
            step_type = st.selectbox(
                "Tipo",
                options=[
                    "Manual", "Automático", "Decisão",
                    "Validação", "Integração", "Outro"
                ],
                key="new_step_type",
                help="Tipo do passo"
            )
        
        # Responsável e sistema
        col1, col2 = st.columns(2)
        
        with col1:
            actor = st.text_input(
                "Responsável",
                key="new_step_actor",
                help="Quem executa este passo"
            )
        
        with col2:
            system = st.text_input(
                "Sistema",
                key="new_step_system",
                help="Sistema utilizado"
            )
        
        # Entradas e saídas
        col1, col2 = st.columns(2)
        
        with col1:
            inputs = st.text_area(
                "Entradas",
                key="new_step_inputs",
                help="Dados/documentos necessários"
            )
        
        with col2:
            outputs = st.text_area(
                "Saídas",
                key="new_step_outputs",
                help="Dados/documentos gerados"
            )
        
        if st.button("➕ Adicionar Passo", use_container_width=True):
            self._add_step(description, step_type, actor, system, inputs, outputs)
            st.rerun()
        
        # Lista de passos
        st.write("#### Passos Cadastrados")
        for i, step in enumerate(st.session_state.steps_list):
            with st.container():
                # Cabeçalho do passo
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**Passo {step['order']}: {step['type']}**")
                
                with col2:
                    if i > 0:
                        if st.button("⬆️", key=f"up_{i}"):
                            self._move_step(i, -1)
                            st.rerun()
                
                with col3:
                    if i < len(st.session_state.steps_list) - 1:
                        if st.button("⬇️", key=f"down_{i}"):
                            self._move_step(i, 1)
                            st.rerun()
                
                # Detalhes do passo
                st.write(step['description'])
                st.write(f"🧑‍💼 Responsável: {step['actor']} | 💻 Sistema: {step['system']}")
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if step.get('inputs'):
                        st.write("📥 Entradas:", step['inputs'])
                    if step.get('outputs'):
                        st.write("📤 Saídas:", step['outputs'])
                
                with col2:
                    if st.button("🗑️", key=f"del_step_{i}"):
                        self._remove_step(i)
                        st.rerun()
                
                st.divider()
        
        # Informações adicionais
        st.write("#### Informações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Fluxo do Processo",
                key="process_flow",
                value=self.form_data.data.get("process_flow", ""),
                help="Descreva o fluxo entre os passos"
            )
            
            st.text_area(
                "Pontos de Decisão",
                key="decision_points",
                value=self.form_data.data.get("decision_points", ""),
                help="Liste os pontos de decisão"
            )
        
        with col2:
            st.text_area(
                "Exceções",
                key="exceptions",
                value=self.form_data.data.get("exceptions", ""),
                help="Liste as exceções possíveis"
            )
            
            st.text_area(
                "Validações",
                key="validations",
                value=self.form_data.data.get("validations", ""),
                help="Descreva as validações necessárias"
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
                st.session_state.steps_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.steps_list = []
                st.warning("Edição cancelada")
                st.rerun() 