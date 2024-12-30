"""Módulo do formulário de riscos."""
from typing import Dict, Any, List
import streamlit as st
from .form_base import FormBase

class RisksForm(FormBase):
    """Formulário para riscos e mitigações do processo."""
    
    def __init__(self, container=None):
        """Inicializa o formulário."""
        super().__init__(container)
        self._data: Dict[str, Any] = {}
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        errors = self.validator.validate_form(self._data, "risks")
        if errors:
            for error in errors:
                st.error(error.message)
            return False
        return True
    
    def _add_risk(self, risks: List[Dict[str, Any]]) -> None:
        """Adiciona um novo risco."""
        col1, col2 = st.columns(2)
        with col1:
            description = st.text_area(
                "Descrição do Risco",
                key="new_risk_description",
                help="Descreva o risco identificado"
            )
        with col2:
            impact = st.selectbox(
                "Impacto",
                options=["Baixo", "Médio", "Alto", "Crítico"],
                key="new_risk_impact"
            )
            probability = st.selectbox(
                "Probabilidade",
                options=["Baixa", "Média", "Alta"],
                key="new_risk_probability"
            )
            
        mitigation = st.text_area(
            "Plano de Mitigação",
            key="new_risk_mitigation",
            help="Descreva como o risco será mitigado"
        )
            
        if st.button("➕ Adicionar Risco") and description and mitigation:
            risks.append({
                "description": description,
                "impact": impact,
                "probability": probability,
                "mitigation": mitigation,
                "status": "Identificado"
            })
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### ⚠️ Riscos e Mitigações")
        
        # Inicializa lista se não existir
        if "risks" not in self._data:
            self._data["risks"] = []
            
        # Lista riscos existentes
        risks = self._data["risks"]
        for i, risk in enumerate(risks):
            with st.expander(f"Risco {i+1}: {risk['description'][:50]}..."):
                col1, col2 = st.columns([4, 1])
                with col1:
                    risks[i]["description"] = st.text_area(
                        "Descrição",
                        value=risk["description"],
                        key=f"risk_description_{i}"
                    )
                    
                    col_impact, col_prob, col_status = st.columns(3)
                    with col_impact:
                        risks[i]["impact"] = st.selectbox(
                            "Impacto",
                            options=["Baixo", "Médio", "Alto", "Crítico"],
                            index=["Baixo", "Médio", "Alto", "Crítico"].index(risk["impact"]),
                            key=f"risk_impact_{i}"
                        )
                    with col_prob:
                        risks[i]["probability"] = st.selectbox(
                            "Probabilidade",
                            options=["Baixa", "Média", "Alta"],
                            index=["Baixa", "Média", "Alta"].index(risk["probability"]),
                            key=f"risk_probability_{i}"
                        )
                    with col_status:
                        risks[i]["status"] = st.selectbox(
                            "Status",
                            options=["Identificado", "Em Análise", "Mitigado"],
                            index=["Identificado", "Em Análise", "Mitigado"].index(risk["status"]),
                            key=f"risk_status_{i}"
                        )
                    
                    risks[i]["mitigation"] = st.text_area(
                        "Plano de Mitigação",
                        value=risk["mitigation"],
                        key=f"risk_mitigation_{i}"
                    )
                    
                with col2:
                    if st.button("🗑️", key=f"del_risk_{i}"):
                        risks.pop(i)
                        st.rerun()
        
        # Adicionar novo risco
        self._add_risk(risks)
        
        # Resumo dos riscos
        if risks:
            st.write("#### 📊 Resumo dos Riscos")
            
            # Contagem por impacto
            impact_counts = {
                "Crítico": len([r for r in risks if r["impact"] == "Crítico"]),
                "Alto": len([r for r in risks if r["impact"] == "Alto"]),
                "Médio": len([r for r in risks if r["impact"] == "Médio"]),
                "Baixo": len([r for r in risks if r["impact"] == "Baixo"])
            }
            
            # Contagem por status
            status_counts = {
                "Identificado": len([r for r in risks if r["status"] == "Identificado"]),
                "Em Análise": len([r for r in risks if r["status"] == "Em Análise"]),
                "Mitigado": len([r for r in risks if r["status"] == "Mitigado"])
            }
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("Por Impacto:")
                for impact, count in impact_counts.items():
                    if count > 0:
                        st.write(f"- {impact}: {count}")
                        
            with col2:
                st.write("Por Status:")
                for status, count in status_counts.items():
                    if count > 0:
                        st.write(f"- {status}: {count}") 