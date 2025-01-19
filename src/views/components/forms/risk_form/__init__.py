"""Formulário de riscos e mitigações."""
from typing import Optional, List, Dict
import streamlit as st
from utils.container_interface import ContainerInterface
from ..form_base import BaseForm
from ..form_field import FormField

class RisksForm(BaseForm):
    """Formulário para riscos e mitigações."""
    
    RISK_LEVELS = ["Baixo", "Médio", "Alto", "Crítico"]
    RISK_TYPES = [
        "Operacional", "Tecnológico", "Financeiro", "Legal/Regulatório",
        "Segurança", "Reputacional", "Processo", "Outro"
    ]
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """Inicializa o formulário."""
        super().__init__("risks", container)
        
        # Inicializa campos
        self.risks_field = FormField(self.form_id, "risks")
        self.mitigations_field = FormField(self.form_id, "mitigations")
        self.contingencies_field = FormField(self.form_id, "contingencies")
        
        # Inicializa listas se não existirem
        if "risks_list" not in st.session_state:
            st.session_state.risks_list = self.form_data.data.get("risks", [])
        if "mitigations_list" not in st.session_state:
            st.session_state.mitigations_list = self.form_data.data.get("mitigations", [])
        if "contingencies_list" not in st.session_state:
            st.session_state.contingencies_list = self.form_data.data.get("contingencies", [])
    
    def validate(self) -> bool:
        """Valida os dados do formulário."""
        is_valid = True
        errors = []
        
        # Só valida se a flag de validação estiver ativa
        if not st.session_state[f"{self.form_id}_show_validation"]:
            return True
        
        # Valida riscos
        if not st.session_state.risks_list:
            errors.append("Pelo menos um risco deve ser identificado")
            is_valid = False
        
        # Valida mitigações para riscos altos/críticos
        high_risks = [r for r in st.session_state.risks_list if r["level"] in ["Alto", "Crítico"]]
        risks_with_mitigation = {m["risk_index"] for m in st.session_state.mitigations_list}
        
        for i, risk in enumerate(high_risks):
            if i not in risks_with_mitigation:
                errors.append(f"O risco '{risk['description'][:50]}...' é {risk['level']} e requer plano de mitigação")
                is_valid = False
        
        # Valida contingências para riscos críticos
        critical_risks = [r for r in st.session_state.risks_list if r["level"] == "Crítico"]
        risks_with_contingency = {c["risk_index"] for c in st.session_state.contingencies_list}
        
        for i, risk in enumerate(critical_risks):
            if i not in risks_with_contingency:
                errors.append(f"O risco '{risk['description'][:50]}...' é Crítico e requer plano de contingência")
                is_valid = False
        
        # Mostra erros se houver
        for error in errors:
            st.error(error)
        
        return is_valid
    
    def _add_risk(self) -> None:
        """Adiciona um novo risco."""
        col1, col2 = st.columns(2)
        with col1:
            risk_type = st.selectbox(
                "Tipo de Risco",
                options=self.RISK_TYPES,
                key="new_risk_type"
            )
        with col2:
            level = st.selectbox(
                "Nível de Risco",
                options=self.RISK_LEVELS,
                key="new_risk_level"
            )
            
        description = st.text_area(
            "Descrição do Risco",
            key="new_risk_desc",
            help="Descreva o risco e seu impacto potencial"
        )
        
        impact = st.text_area(
            "Impacto",
            key="new_risk_impact",
            help="Descreva o impacto caso o risco se materialize"
        )
            
        if st.button("➕ Adicionar Risco"):
            if risk_type and level and description and impact:
                new_risk = {
                    "type": risk_type,
                    "level": level,
                    "description": description,
                    "impact": impact
                }
                st.session_state.risks_list.append(new_risk)
                self.update_field("risks", st.session_state.risks_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_mitigation(self) -> None:
        """Adiciona um novo plano de mitigação."""
        if not st.session_state.risks_list:
            st.warning("Adicione riscos primeiro")
            return
            
        risk_options = [f"{r['type']} - {r['description'][:50]}..." for r in st.session_state.risks_list]
        risk_index = st.selectbox(
            "Risco Relacionado",
            options=range(len(risk_options)),
            format_func=lambda x: risk_options[x],
            key="new_mitigation_risk"
        )
        
        strategy = st.text_area(
            "Estratégia de Mitigação",
            key="new_mitigation_strategy",
            help="Descreva as ações para reduzir a probabilidade ou impacto"
        )
        
        responsible = st.text_input(
            "Responsável",
            key="new_mitigation_responsible"
        )
            
        if st.button("➕ Adicionar Mitigação"):
            if strategy and responsible:
                new_mitigation = {
                    "risk_index": risk_index,
                    "strategy": strategy,
                    "responsible": responsible
                }
                st.session_state.mitigations_list.append(new_mitigation)
                self.update_field("mitigations", st.session_state.mitigations_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def _add_contingency(self) -> None:
        """Adiciona um novo plano de contingência."""
        if not st.session_state.risks_list:
            st.warning("Adicione riscos primeiro")
            return
            
        risk_options = [f"{r['type']} - {r['description'][:50]}..." for r in st.session_state.risks_list]
        risk_index = st.selectbox(
            "Risco Relacionado",
            options=range(len(risk_options)),
            format_func=lambda x: risk_options[x],
            key="new_contingency_risk"
        )
        
        plan = st.text_area(
            "Plano de Contingência",
            key="new_contingency_plan",
            help="Descreva as ações caso o risco se materialize"
        )
        
        trigger = st.text_input(
            "Gatilho",
            key="new_contingency_trigger",
            help="Quando este plano deve ser acionado?"
        )
            
        if st.button("➕ Adicionar Contingência"):
            if plan and trigger:
                new_contingency = {
                    "risk_index": risk_index,
                    "plan": plan,
                    "trigger": trigger
                }
                st.session_state.contingencies_list.append(new_contingency)
                self.update_field("contingencies", st.session_state.contingencies_list)
                st.rerun()
            else:
                st.error("Preencha todos os campos")
    
    def render(self) -> None:
        """Renderiza o formulário."""
        self.render_form_header("⚠️ Riscos e Mitigações")
        
        # Seção de Riscos
        st.write("#### Riscos Identificados")
        
        # Lista riscos existentes
        for i, risk in enumerate(st.session_state.risks_list):
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_type = st.selectbox(
                    "Tipo",
                    options=self.RISK_TYPES,
                    index=self.RISK_TYPES.index(risk["type"]),
                    key=f"risk_type_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_level = st.selectbox(
                    "Nível",
                    options=self.RISK_LEVELS,
                    index=self.RISK_LEVELS.index(risk["level"]),
                    key=f"risk_level_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_risk_{i}"):
                    st.session_state.risks_list.pop(i)
                    self.update_field("risks", st.session_state.risks_list)
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                new_description = st.text_area(
                    "Descrição",
                    value=risk["description"],
                    key=f"risk_desc_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_impact = st.text_area(
                    "Impacto",
                    value=risk["impact"],
                    key=f"risk_impact_{i}",
                    disabled=not self.is_editing
                )
            
            if self.is_editing and (
                new_type != risk["type"] or
                new_level != risk["level"] or
                new_description != risk["description"] or
                new_impact != risk["impact"]
            ):
                st.session_state.risks_list[i] = {
                    "type": new_type,
                    "level": new_level,
                    "description": new_description,
                    "impact": new_impact
                }
                self.update_field("risks", st.session_state.risks_list)
        
        # Adicionar novo risco
        if self.is_editing:
            self._add_risk()
        
        # Seção de Mitigações
        st.write("#### Planos de Mitigação")
        
        # Lista mitigações existentes
        for i, mitigation in enumerate(st.session_state.mitigations_list):
            st.markdown("---")
            
            # Mostra o risco relacionado
            risk = st.session_state.risks_list[mitigation["risk_index"]]
            st.write(f"**Risco:** {risk['type']} - {risk['description'][:100]}...")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_strategy = st.text_area(
                    "Estratégia",
                    value=mitigation["strategy"],
                    key=f"mitigation_strategy_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_responsible = st.text_input(
                    "Responsável",
                    value=mitigation["responsible"],
                    key=f"mitigation_responsible_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_mitigation_{i}"):
                    st.session_state.mitigations_list.pop(i)
                    self.update_field("mitigations", st.session_state.mitigations_list)
                    st.rerun()
            
            if self.is_editing and (
                new_strategy != mitigation["strategy"] or
                new_responsible != mitigation["responsible"]
            ):
                st.session_state.mitigations_list[i] = {
                    "risk_index": mitigation["risk_index"],
                    "strategy": new_strategy,
                    "responsible": new_responsible
                }
                self.update_field("mitigations", st.session_state.mitigations_list)
        
        # Adicionar nova mitigação
        if self.is_editing:
            self._add_mitigation()
        
        # Seção de Contingências
        st.write("#### Planos de Contingência")
        
        # Lista contingências existentes
        for i, contingency in enumerate(st.session_state.contingencies_list):
            st.markdown("---")
            
            # Mostra o risco relacionado
            risk = st.session_state.risks_list[contingency["risk_index"]]
            st.write(f"**Risco:** {risk['type']} - {risk['description'][:100]}...")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_plan = st.text_area(
                    "Plano",
                    value=contingency["plan"],
                    key=f"contingency_plan_{i}",
                    disabled=not self.is_editing
                )
            with col2:
                new_trigger = st.text_input(
                    "Gatilho",
                    value=contingency["trigger"],
                    key=f"contingency_trigger_{i}",
                    disabled=not self.is_editing
                )
            with col3:
                if self.is_editing and st.button("🗑️", key=f"del_contingency_{i}"):
                    st.session_state.contingencies_list.pop(i)
                    self.update_field("contingencies", st.session_state.contingencies_list)
                    st.rerun()
            
            if self.is_editing and (
                new_plan != contingency["plan"] or
                new_trigger != contingency["trigger"]
            ):
                st.session_state.contingencies_list[i] = {
                    "risk_index": contingency["risk_index"],
                    "plan": new_plan,
                    "trigger": new_trigger
                }
                self.update_field("contingencies", st.session_state.contingencies_list)
        
        # Adicionar nova contingência
        if self.is_editing:
            self._add_contingency() 