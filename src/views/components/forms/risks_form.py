"""Formulário de riscos do processo."""
from typing import Optional, Dict, Any, List
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager, FormState

class RisksForm:
    """Formulário de riscos do processo."""
    
    IMPACT_LEVELS = ["Alto", "Médio", "Baixo"]
    PROBABILITY_LEVELS = ["Alta", "Média", "Baixa"]
    RISK_TYPES = [
        "Operacional", "Tecnológico", "Financeiro", 
        "Compliance", "Segurança", "Outro"
    ]
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa o formulário.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()
        self.form_id = "risks"
        
        # Carrega dados existentes
        self.form_data = self.state_manager.get_form_data(self.form_id)
        
        # Inicializa lista de riscos se necessário
        if "risks_list" not in st.session_state:
            st.session_state.risks_list = self.form_data.data.get("risks", [])
    
    def validate(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se válido, False caso contrário
        """
        data = self.get_data()
        risks = data.get("risks", [])
        
        if not risks:
            st.error("Adicione pelo menos um risco")
            return False
        
        for risk in risks:
            if not risk.get("description"):
                st.error("Todos os riscos precisam ter uma descrição")
                return False
            if not risk.get("type"):
                st.error("Todos os riscos precisam ter um tipo")
                return False
            if not risk.get("impact"):
                st.error("Todos os riscos precisam ter um impacto definido")
                return False
            if not risk.get("probability"):
                st.error("Todos os riscos precisam ter uma probabilidade definida")
                return False
        
        return True
    
    def get_data(self) -> Dict[str, Any]:
        """
        Obtém os dados do formulário.
        
        Returns:
            Dict[str, Any]: Dados do formulário
        """
        return {
            "risks": st.session_state.risks_list,
            "risk_assessment": st.session_state.get("risk_assessment", ""),
            "mitigation_strategy": st.session_state.get("mitigation_strategy", ""),
            "contingency_plan": st.session_state.get("contingency_plan", ""),
            "monitoring_plan": st.session_state.get("monitoring_plan", "")
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
    
    def _calculate_risk_level(self, impact: str, probability: str) -> str:
        """
        Calcula o nível de risco com base no impacto e probabilidade.
        
        Args:
            impact: Nível de impacto
            probability: Nível de probabilidade
            
        Returns:
            str: Nível de risco (Alto, Médio ou Baixo)
        """
        # Matriz de risco 3x3
        risk_matrix = {
            ("Alto", "Alta"): "Alto",
            ("Alto", "Média"): "Alto",
            ("Alto", "Baixa"): "Médio",
            ("Médio", "Alta"): "Alto",
            ("Médio", "Média"): "Médio",
            ("Médio", "Baixa"): "Baixo",
            ("Baixo", "Alta"): "Médio",
            ("Baixo", "Média"): "Baixo",
            ("Baixo", "Baixa"): "Baixo"
        }
        
        return risk_matrix.get((impact, probability), "Médio")
    
    def _get_risk_color(self, level: str) -> str:
        """
        Retorna a cor para o nível de risco.
        
        Args:
            level: Nível de risco
            
        Returns:
            str: Código de cor HTML
        """
        colors = {
            "Alto": "#ff4b4b",
            "Médio": "#ffa64b",
            "Baixo": "#4bff4b"
        }
        return colors.get(level, "#ffffff")
    
    def _add_risk(
        self,
        description: str,
        risk_type: str,
        impact: str,
        probability: str,
        mitigation: str
    ) -> None:
        """
        Adiciona um novo risco à lista.
        
        Args:
            description: Descrição do risco
            risk_type: Tipo do risco
            impact: Nível de impacto
            probability: Nível de probabilidade
            mitigation: Medidas de mitigação
        """
        if not description:
            st.error("Descrição do risco é obrigatória")
            return
            
        if not risk_type:
            st.error("Tipo do risco é obrigatório")
            return
        
        # Calcula nível de risco
        risk_level = self._calculate_risk_level(impact, probability)
        
        new_risk = {
            "description": description,
            "type": risk_type,
            "impact": impact,
            "probability": probability,
            "level": risk_level,
            "mitigation": mitigation
        }
        
        st.session_state.risks_list.append(new_risk)
        st.session_state.new_risk_description = ""
        st.session_state.new_risk_type = ""
        st.session_state.new_risk_impact = ""
        st.session_state.new_risk_probability = ""
        st.session_state.new_risk_mitigation = ""
    
    def _remove_risk(self, index: int) -> None:
        """
        Remove um risco da lista.
        
        Args:
            index: Índice do risco a ser removido
        """
        st.session_state.risks_list.pop(index)
    
    def render(self) -> None:
        """Renderiza o formulário."""
        st.write("### ⚠️ Riscos do Processo")
        
        # Adicionar novo risco
        st.write("#### Adicionar Novo Risco")
        
        # Descrição e tipo
        col1, col2 = st.columns([3, 1])
        
        with col1:
            description = st.text_area(
                "Descrição do Risco",
                key="new_risk_description",
                help="Descreva o risco identificado"
            )
        
        with col2:
            risk_type = st.selectbox(
                "Tipo",
                options=self.RISK_TYPES,
                key="new_risk_type",
                help="Tipo do risco"
            )
        
        # Impacto e probabilidade
        col1, col2 = st.columns(2)
        
        with col1:
            impact = st.selectbox(
                "Impacto",
                options=self.IMPACT_LEVELS,
                key="new_risk_impact",
                help="Nível de impacto"
            )
        
        with col2:
            probability = st.selectbox(
                "Probabilidade",
                options=self.PROBABILITY_LEVELS,
                key="new_risk_probability",
                help="Probabilidade de ocorrência"
            )
        
        # Mitigação
        mitigation = st.text_area(
            "Medidas de Mitigação",
            key="new_risk_mitigation",
            help="Descreva as medidas para mitigar este risco"
        )
        
        if st.button("➕ Adicionar Risco", use_container_width=True):
            self._add_risk(description, risk_type, impact, probability, mitigation)
            st.rerun()
        
        # Lista de riscos
        st.write("#### Riscos Cadastrados")
        for i, risk in enumerate(st.session_state.risks_list):
            with st.container():
                # Cabeçalho do risco
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(
                        f"**{risk['type']}** | "
                        f"<span style='color: {self._get_risk_color(risk['level'])}'>⬤</span> "
                        f"Nível: {risk['level']}",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    if st.button("🗑️", key=f"del_risk_{i}"):
                        self._remove_risk(i)
                        st.rerun()
                
                # Detalhes do risco
                st.write(risk['description'])
                st.write(
                    f"📊 Impacto: {risk['impact']} | "
                    f"📈 Probabilidade: {risk['probability']}"
                )
                if risk.get('mitigation'):
                    st.write("🛡️ Mitigação:", risk['mitigation'])
                
                st.divider()
        
        # Informações adicionais
        st.write("#### Informações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "Avaliação de Riscos",
                key="risk_assessment",
                value=self.form_data.data.get("risk_assessment", ""),
                help="Avaliação geral dos riscos"
            )
            
            st.text_area(
                "Estratégia de Mitigação",
                key="mitigation_strategy",
                value=self.form_data.data.get("mitigation_strategy", ""),
                help="Estratégia geral de mitigação"
            )
        
        with col2:
            st.text_area(
                "Plano de Contingência",
                key="contingency_plan",
                value=self.form_data.data.get("contingency_plan", ""),
                help="Plano para caso os riscos se concretizem"
            )
            
            st.text_area(
                "Plano de Monitoramento",
                key="monitoring_plan",
                value=self.form_data.data.get("monitoring_plan", ""),
                help="Como os riscos serão monitorados"
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
                st.session_state.risks_list = []
                st.rerun()
        
        with col3:
            if st.button("❌ Cancelar", use_container_width=True):
                self.state_manager.clear_form(self.form_id)
                st.session_state.risks_list = []
                st.warning("Edição cancelada")
                st.rerun() 