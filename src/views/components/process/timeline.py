"""Módulo da timeline do processo."""
from typing import List, Optional
import streamlit as st
from dataclasses import dataclass
from enum import Enum

class StepStatus(Enum):
    """Status possíveis de um passo."""
    PENDING = "pending"
    CURRENT = "current"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class TimelineStep:
    """Representa um passo na timeline."""
    id: str
    title: str
    description: str
    status: StepStatus
    icon: str
    order: int
    is_required: bool = True
    validation_errors: Optional[List[str]] = None

class ProcessTimeline:
    """Timeline do processo de documentação."""
    
    def __init__(self):
        """Inicializa a timeline."""
        self.steps = [
            TimelineStep(
                id="identification",
                title="Identificação",
                description="Dados básicos",
                status=StepStatus.CURRENT,
                icon="📋",
                order=1
            ),
            TimelineStep(
                id="details",
                title="Detalhes",
                description="Informações detalhadas",
                status=StepStatus.PENDING,
                icon="ℹ️",
                order=2
            ),
            TimelineStep(
                id="rules",
                title="Regras",
                description="Regras de negócio",
                status=StepStatus.PENDING,
                icon="📜",
                order=3
            ),
            TimelineStep(
                id="goals",
                title="Objetivos",
                description="Objetivos e métricas",
                status=StepStatus.PENDING,
                icon="🎯",
                order=4
            )
        ]
    
    def render(self) -> None:
        """Renderiza a timeline."""
        st.write("### 📅 Progresso")
        
        # Calcula progresso
        completed = len([s for s in self.steps if s.status == StepStatus.COMPLETED])
        progress = completed / len(self.steps)
        
        # Barra de progresso
        st.progress(progress)
        
        # Lista de passos
        for step in self.steps:
            self._render_step(step)
    
    def _render_step(self, step: TimelineStep) -> None:
        """Renderiza um passo da timeline."""
        # Define estilo baseado no status
        if step.status == StepStatus.CURRENT:
            prefix = "🔵"
        elif step.status == StepStatus.COMPLETED:
            prefix = "✅"
        elif step.status == StepStatus.ERROR:
            prefix = "❌"
        else:
            prefix = "⚪"
        
        # Renderiza o passo
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"{prefix} {step.icon}")
        with col2:
            st.write(f"**{step.title}**")
            st.caption(step.description)
            
            # Mostra erros se houver
            if step.validation_errors:
                with st.expander("⚠️ Erros de validação"):
                    for error in step.validation_errors:
                        st.error(error) 