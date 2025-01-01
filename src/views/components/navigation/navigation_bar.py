"""Módulo para barra de navegação."""
from typing import Optional
import streamlit as st
from utils.container_interface import ContainerInterface
from views.components.state.state_manager import StateManager

class NavigationBar:
    """Barra de navegação do processo."""
    
    def __init__(self, container: Optional[ContainerInterface] = None):
        """
        Inicializa a barra de navegação.
        
        Args:
            container: Container de dependências opcional
        """
        self.container = container
        self.state_manager = StateManager()  # Cria uma instância própria
        
        # Define os itens de navegação
        self.nav_items = [
            {
                "id": "identification",
                "title": "Identificação",
                "icon": "🎯",
                "order": 1,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "details",
                "title": "Detalhes",
                "icon": "📋",
                "order": 2,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "rules",
                "title": "Regras",
                "icon": "📜",
                "order": 3,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "systems",
                "title": "Sistemas",
                "icon": "💻",
                "order": 4,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "data",
                "title": "Dados",
                "icon": "📊",
                "order": 5,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "steps",
                "title": "Passos",
                "icon": "👣",
                "order": 6,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "goals",
                "title": "Objetivos",
                "icon": "🎯",
                "order": 7,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "risks",
                "title": "Riscos",
                "icon": "⚠️",
                "order": 8,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            },
            {
                "id": "documentation",
                "title": "Documentação",
                "icon": "📚",
                "order": 9,
                "is_active": False,
                "has_errors": False,
                "is_completed": False
            }
        ]
    
    def _update_nav_states(self) -> None:
        """Atualiza o estado dos itens de navegação."""
        current_form = self.state_manager.get_current_form()
        
        for item in self.nav_items:
            # Atualiza estado ativo
            item["is_active"] = item["id"] == current_form
            
            # Verifica se tem erros
            form_data = self.state_manager.get_form_data(item["id"])
            item["has_errors"] = not form_data.is_valid
            
            # Verifica se está completo
            item["is_completed"] = bool(form_data.data) and form_data.is_valid
    
    def render_sidebar(self) -> None:
        """Renderiza navegação na sidebar."""
        # Atualiza estados
        self._update_nav_states()
        
        st.sidebar.write("### 📍 Navegação")
        
        # Renderiza itens
        for item in self.nav_items:
            # Define estilo do item
            style = "color: blue;" if item["is_active"] else ""
            style += "text-decoration: line-through;" if item["is_completed"] else ""
            
            # Ícone de status
            status = "✅" if item["is_completed"] else "❌" if item["has_errors"] else "⚪"
            
            # Renderiza item clicável
            if st.sidebar.button(
                f"{item['icon']} {item['title']} {status}",
                key=f"side_nav_{item['id']}",
                help=f"Ir para {item['title']}",
                use_container_width=True,
                disabled=item["is_active"]
            ):
                self.state_manager.navigate_to(item["id"])
                st.rerun()
    
    def render_tabs(self) -> None:
        """Renderiza abas de navegação."""
        # Atualiza estados
        self._update_nav_states()
        
        # Cria tabs
        tabs = st.tabs([
            f"{item['icon']} {item['title']}" + 
            (" ❌" if item["has_errors"] else " ✅" if item["is_completed"] else "")
            for item in self.nav_items
        ])
        
        # Adiciona conteúdo das tabs
        for i, (tab, item) in enumerate(zip(tabs, self.nav_items)):
            with tab:
                if item["is_active"]:
                    st.info(f"**{item['title']}**")
                    if item["has_errors"]:
                        st.error("Este formulário contém erros")
                    elif item["is_completed"]:
                        st.success("Formulário completo e válido")
                    else:
                        st.warning("Formulário em edição")
                else:
                    if st.button(
                        "Ir para " + item["title"],
                        key=f"nav_btn_{item['id']}",
                        use_container_width=True
                    ):
                        self.state_manager.navigate_to(item["id"])
                        st.rerun()
    
    def render(self, style: str = "tabs") -> None:
        """
        Renderiza a navegação no estilo especificado.
        
        Args:
            style: Estilo de navegação ("tabs", "sidebar", "breadcrumbs")
        """
        if style == "tabs":
            self.render_tabs()
        elif style == "sidebar":
            self.render_sidebar()
        else:
            raise ValueError(f"Estilo de navegação inválido: {style}") 