"""Módulo principal da aplicação."""
import streamlit as st
from src.utils.dependency_container import DependencyContainer
from src.controllers.process_controller import ProcessController
from src.views.components.process_form import ProcessForm
from src.views.components.process_diagram import ProcessDiagram
from src.utils.config import Config

def main():
    """Função principal da aplicação."""
    st.set_page_config(
        page_title="Agente Analista de RPA",
        page_icon="🤖",
        layout="wide"
    )
    
    # Inicializa container de dependências
    container = DependencyContainer()
    
    # Inicializa componentes com o container
    controller = ProcessController(container)
    process_form = ProcessForm(container)
    process_diagram = ProcessDiagram(container)
    
    # Carrega configurações
    config = container.resolve(Config)
    
    # Renderiza interface
    st.title("🤖 Agente Analista de RPA")
    st.write(config.get_app_description())
    
    # Tabs principais
    tab1, tab2 = st.tabs(["📝 Formulário", "📊 Diagrama"])
    
    with tab1:
        process_form.render()
        
    with tab2:
        process_diagram.render()
        
    # Rodapé
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center'>v{config.get_app_version()} | "
        "Desenvolvido pela Equipe de Automação</div>",
        unsafe_allow_html=True
    )

def handle_process_save(data: dict):
    """Manipula o salvamento do processo."""
    try:
        container = DependencyContainer()
        controller = ProcessController(container)
        if controller.create_process(data):
            st.success("Processo salvo com sucesso!")
            return True
        else:
            st.error("Erro ao salvar processo")
            return False
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return False

def handle_process_update(process_id: str, data: dict):
    """Manipula a atualização do processo."""
    try:
        container = DependencyContainer()
        controller = ProcessController(container)
        if controller.update_process(process_id, data):
            st.success("Processo atualizado com sucesso!")
            return True
        else:
            st.error("Erro ao atualizar processo")
            return False
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return False

def handle_process_delete(process_id: str):
    """Manipula a exclusão do processo."""
    try:
        container = DependencyContainer()
        controller = ProcessController(container)
        if controller.delete_process(process_id):
            st.success("Processo excluído com sucesso!")
            return True
        else:
            st.error("Erro ao excluir processo")
            return False
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return False

if __name__ == "__main__":
    main()
