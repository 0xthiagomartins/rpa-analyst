"""Componente de sumário de validação."""
from typing import Dict, List, Optional, Any
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class ValidationSummary:
    """Sumário de validação dos formulários."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o sumário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
    
    def get_form_validation(self, form_id: str) -> Dict[str, bool]:
        """
        Obtém o status de validação de um formulário.
        
        Args:
            form_id: ID do formulário
            
        Returns:
            Dict[str, bool]: Status de validação
        """
        form_data = self.state_manager.get_form_data(form_id)
        
        return {
            "has_data": bool(form_data.data),
            "is_valid": form_data.is_valid,
            "is_complete": form_data.state == FormState.COMPLETED
        }
    
    def get_all_validations(self) -> List[Dict[str, Any]]:
        """
        Obtém validações de todos os formulários.
        
        Returns:
            List[Dict[str, Any]]: Lista de validações
        """
        forms = [
            {
                "id": "identification",
                "title": "Identificação",
                "icon": "🎯"
            },
            {
                "id": "details",
                "title": "Detalhes",
                "icon": "📋"
            },
            {
                "id": "rules",
                "title": "Regras",
                "icon": "📜"
            },
            {
                "id": "systems",
                "title": "Sistemas",
                "icon": "💻"
            },
            {
                "id": "data",
                "title": "Dados",
                "icon": "📊"
            },
            {
                "id": "steps",
                "title": "Passos",
                "icon": "👣"
            },
            {
                "id": "automation",
                "title": "Automação",
                "icon": "🤖"
            },
            {
                "id": "risks",
                "title": "Riscos",
                "icon": "⚠️"
            },
            {
                "id": "documentation",
                "title": "Documentação",
                "icon": "📚"
            }
        ]
        
        validations = []
        for form in forms:
            validation = self.get_form_validation(form["id"])
            validations.append({
                **form,
                **validation
            })
        
        return validations
    
    def render(self) -> None:
        """Renderiza o sumário de validação."""
        validations = self.get_all_validations()
        
        # Calcula progresso geral
        total_forms = len(validations)
        completed_forms = sum(1 for v in validations if v["is_complete"])
        progress = completed_forms / total_forms if total_forms > 0 else 0
        
        # Mostra progresso geral
        st.progress(progress)
        st.caption(f"Progresso: {progress*100:.0f}% ({completed_forms}/{total_forms})")
        
        # Lista status de cada formulário
        for validation in validations:
            status = "✅" if validation["is_complete"] else "❌" if validation["has_data"] and not validation["is_valid"] else "⚪"
            st.write(f"{validation['icon']} {validation['title']}: {status}") 