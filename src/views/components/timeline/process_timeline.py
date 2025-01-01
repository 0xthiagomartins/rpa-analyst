"""Módulo para visualização do timeline do processo."""
from typing import List, Dict, Any, Optional
import streamlit as st
from dataclasses import dataclass
from enum import Enum
from src.views.components.state.state_manager import StateManager

class StepStatus(Enum):
    """Status possíveis de um passo do processo."""
    PENDING = "pending"
    CURRENT = "current"
    COMPLETED = "completed"
    ERROR = "error"
    SKIPPED = "skipped"

@dataclass
class TimelineStep:
    """Representa um passo no timeline."""
    id: str
    title: str
    description: str
    status: StepStatus
    icon: str
    order: int
    is_required: bool = True
    validation_errors: Optional[List[str]] = None

class ProcessTimeline:
    """Componente para visualização do progresso do processo."""
    
    def __init__(self, state_manager: Optional[StateManager] = None):
        """Inicializa o timeline."""
        self.state_manager = state_manager or StateManager()
        
        # Define os passos do processo
        self.steps = [
            TimelineStep(
                id="identification",
                title="Identificação",
                description="Informações básicas do processo",
                status=StepStatus.PENDING,
                icon="🎯",
                order=1
            ),
            TimelineStep(
                id="details",
                title="Detalhes",
                description="Detalhamento do processo",
                status=StepStatus.PENDING,
                icon="📋",
                order=2
            ),
            TimelineStep(
                id="rules",
                title="Regras",
                description="Regras de negócio e exceções",
                status=StepStatus.PENDING,
                icon="📜",
                order=3
            ),
            TimelineStep(
                id="systems",
                title="Sistemas",
                description="Sistemas e integrações",
                status=StepStatus.PENDING,
                icon="💻",
                order=4
            ),
            TimelineStep(
                id="data",
                title="Dados",
                description="Dados e arquivos",
                status=StepStatus.PENDING,
                icon="📊",
                order=5
            ),
            TimelineStep(
                id="steps",
                title="Passos",
                description="Fluxo do processo",
                status=StepStatus.PENDING,
                icon="👣",
                order=6
            ),
            TimelineStep(
                id="automation",
                title="Automação",
                description="Objetivos e KPIs",
                status=StepStatus.PENDING,
                icon="🤖",
                order=7
            ),
            TimelineStep(
                id="risks",
                title="Riscos",
                description="Riscos e mitigações",
                status=StepStatus.PENDING,
                icon="⚠️",
                order=8,
                is_required=False
            ),
            TimelineStep(
                id="documentation",
                title="Documentação",
                description="Documentação e anexos",
                status=StepStatus.PENDING,
                icon="📚",
                order=9
            )
        ]
    
    def update_step_status(self, step_id: str, status: StepStatus, 
                          errors: Optional[List[str]] = None) -> None:
        """Atualiza o status de um passo."""
        for step in self.steps:
            if step.id == step_id:
                step.status = status
                step.validation_errors = errors
                break
    
    def get_current_step(self) -> Optional[TimelineStep]:
        """Retorna o passo atual."""
        current_form = self.state_manager.get_current_form()
        if not current_form:
            return None
        
        for step in self.steps:
            if step.id == current_form:
                return step
        return None
    
    def get_next_step(self) -> Optional[TimelineStep]:
        """Retorna o próximo passo disponível."""
        current = self.get_current_step()
        if not current:
            return self.steps[0]
            
        next_steps = [s for s in self.steps if s.order > current.order]
        return next_steps[0] if next_steps else None
    
    def get_previous_step(self) -> Optional[TimelineStep]:
        """Retorna o passo anterior."""
        current = self.get_current_step()
        if not current or current.order <= 1:
            return None
            
        prev_steps = [s for s in self.steps if s.order < current.order]
        return prev_steps[-1] if prev_steps else None
    
    def render(self) -> None:
        """Renderiza o timeline."""
        st.write("### 📋 Progresso do Processo")
        
        # Calcula progresso geral
        completed = len([s for s in self.steps if s.status == StepStatus.COMPLETED])
        total = len([s for s in self.steps if s.is_required])
        progress = completed / total if total > 0 else 0
        
        # Barra de progresso
        st.progress(progress)
        st.caption(f"{int(progress * 100)}% concluído")
        
        # Lista de passos
        for step in sorted(self.steps, key=lambda x: x.order):
            col1, col2 = st.columns([0.1, 0.9])
            
            with col1:
                st.write(step.icon)
                
            with col2:
                # Título com status
                status_icon = {
                    StepStatus.PENDING: "⚪",
                    StepStatus.CURRENT: "🔵",
                    StepStatus.COMPLETED: "✅",
                    StepStatus.ERROR: "❌",
                    StepStatus.SKIPPED: "⏭️"
                }[step.status]
                
                st.write(f"**{status_icon} {step.title}**")
                st.caption(step.description)
                
                # Mostra erros se houver
                if step.validation_errors:
                    with st.expander("⚠️ Erros de validação"):
                        for error in step.validation_errors:
                            st.error(error)
                
                # Botão de navegação se for o passo atual
                if step.status == StepStatus.CURRENT:
                    st.button(
                        "📝 Continuar",
                        key=f"btn_continue_{step.id}",
                        on_click=lambda: self.state_manager.navigate_to(step.id)
                    ) 