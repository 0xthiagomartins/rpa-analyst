from typing import List, Dict
import streamlit as st
from streamlit_mermaid import st_mermaid
from src.services.mermaid_service import MermaidService

def render_process_diagram(steps: List[Dict] = None):
    """Renderiza o diagrama do processo usando Mermaid."""
    if not steps:
        steps = st.session_state.get('process_steps', [])
    
    if not steps:
        st.info("Nenhuma etapa definida ainda.")
        return
    
    # Gera o código Mermaid
    mermaid_code = generate_mermaid_diagram(steps)
    
    # Valida o código
    mermaid_service = MermaidService()
    if not mermaid_service.validate_mermaid_syntax(mermaid_code):
        st.warning("⚠️ O diagrama gerado pode conter erros de sintaxe")
    
    # Renderiza o diagrama
    st.write("### 📊 Diagrama do Processo")
    st_mermaid(mermaid_code)

def generate_mermaid_diagram(steps: List[Dict]) -> str:
    """Gera o código Mermaid para o diagrama."""
    mermaid_lines = ["flowchart TD"]
    
    # Adiciona os nós
    for step in steps:
        node_id = step['id']
        # Sanitiza o texto do nó
        node_label = step['name'].replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
        node_type = step.get('type', 'action')
        
        # Adiciona o nó com estilo baseado no tipo
        mermaid_lines.append(f"    {node_id}[\"{node_label}\"]:::{node_type}")
    
    # Adiciona as conexões baseadas nas dependências
    for step in steps:
        for dep in step.get('dependencies', []):
            mermaid_lines.append(f"    {dep} --> {step['id']}")
    
    # Adiciona estilos para cada tipo de nó
    mermaid_lines.extend([
        "    classDef action fill:#bbdefb,stroke:#333,stroke-width:2px",
        "    classDef decision fill:#fff59d,stroke:#333,stroke-width:2px",
        "    classDef system fill:#c8e6c9,stroke:#333,stroke-width:2px",
        "    classDef start fill:#f9f9f9,stroke:#333,stroke-width:2px",
        "    classDef end fill:#f9f9f9,stroke:#333,stroke-width:2px"
    ])
    
    return "\n".join(mermaid_lines) 