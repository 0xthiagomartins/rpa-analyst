# Sprint 9 - Editor de Fluxo e Diagramas

## Objetivo
Implementar um editor visual de fluxo de processo com geração de diagramas usando Mermaid, permitindo a edição intuitiva das conexões entre passos.

## Status Atual
🟡 Não Iniciado (0%)

## Fases de Implementação

### Fase 1: Estrutura Base
1. **Componentes Base**
   - [ ] Criar FlowEditor
   - [ ] Implementar FlowchartGenerator
   - [ ] Desenvolver DiagramViewer
   - [ ] Criar FlowValidator

2. **Integração com StepsForm**
   - [ ] Adicionar botão "Editar Fluxo"
   - [ ] Implementar transição de dados
   - [ ] Sincronizar alterações
   - [ ] Validar consistência

### Fase 2: Editor Visual
1. **Interface do Editor**
   - [ ] Layout base do editor
   - [ ] Lista de passos editável
   - [ ] Preview do diagrama
   - [ ] Controles de edição

2. **Gerenciamento de Conexões**
   - [ ] Interface de conexões
   - [ ] Validação em tempo real
   - [ ] Feedback visual
   - [ ] Tratamento de erros

3. **Persistência de Layout**
   - [ ] Salvar posições dos elementos
   - [ ] Restaurar layout
   - [ ] Gerenciar estado do editor
   - [ ] Auto-organização

### Fase 3: Geração de Diagramas
1. **Mermaid Integration**
   - [ ] Templates de símbolos
   - [ ] Geração de código
   - [ ] Renderização em tempo real
   - [ ] Exportação

2. **Validações**
   - [ ] Verificar ciclos
   - [ ] Validar conexões
   - [ ] Checar passos órfãos
   - [ ] Validar fluxo completo

## Componentes Principais

### 1. FlowEditor
```python
class FlowEditor:
    """Editor visual de fluxo do processo."""
    
    def __init__(self):
        self.generator = FlowchartGenerator()
        self.validator = FlowValidator()
        self.layout_manager = LayoutManager()
    
    def render(self):
        """Renderiza o editor."""
        col1, col2 = st.columns([2, 3])
        
        with col1:
            self._render_steps_list()
            self._render_connections_editor()
        
        with col2:
            self._render_diagram_preview()
            self._render_validation_feedback()
    
    def _render_steps_list(self):
        """Lista editável de passos."""
        st.write("### Passos do Processo")
        
        for step in self.get_steps():
            self._render_step_editor(step)
    
    def _render_connections_editor(self):
        """Editor de conexões."""
        st.write("### Conexões")
        
        selected_step = st.selectbox(
            "Selecione o Passo",
            options=self.get_steps(),
            format_func=lambda x: x['description']
        )
        
        if selected_step:
            self._render_step_connections(selected_step)
    
    def _render_diagram_preview(self):
        """Preview do diagrama."""
        st.write("### Diagrama")
        
        try:
            mermaid_code = self.generator.generate_diagram(
                self.get_steps(),
                self.layout_manager.get_layout()
            )
            
            st.markdown(f"""
            ```mermaid
            {mermaid_code}
            ```
            """)
            
        except Exception as e:
            st.error(f"Erro ao gerar diagrama: {str(e)}")
```

### 2. FlowValidator
```python
class FlowValidator:
    """Validador de fluxo do processo."""
    
    def validate_flow(self, steps: List[Dict]) -> List[str]:
        """Valida o fluxo completo."""
        issues = []
        
        # Verifica início/fim
        if not self._has_start_end(steps):
            issues.append("Fluxo precisa ter início e fim")
        
        # Verifica conexões
        orphans = self._find_orphans(steps)
        if orphans:
            issues.append(f"Passos sem conexão: {', '.join(orphans)}")
        
        # Verifica ciclos
        cycles = self._find_cycles(steps)
        if cycles:
            issues.append(f"Ciclos detectados: {cycles}")
        
        return issues
    
    def _has_start_end(self, steps: List[Dict]) -> bool:
        """Verifica se tem início e fim."""
        has_start = any(s['type'] == 'start' for s in steps)
        has_end = any(s['type'] == 'end' for s in steps)
        return has_start and has_end
    
    def _find_orphans(self, steps: List[Dict]) -> List[str]:
        """Encontra passos sem conexões."""
        connected = set()
        for step in steps:
            for conn in step['connections']:
                connected.add(conn['target'])
        
        return [
            step['description'] 
            for step in steps 
            if step['id'] not in connected
        ]
```

### 3. LayoutManager
```python
class LayoutManager:
    """Gerenciador de layout do diagrama."""
    
    def __init__(self):
        self.layout_data = {}
    
    def save_layout(self, layout: Dict):
        """Salva posições dos elementos."""
        self.layout_data.update(layout)
        
    def get_layout(self) -> Dict:
        """Retorna layout atual."""
        return self.layout_data
    
    def auto_organize(self, steps: List[Dict]) -> Dict:
        """Organiza automaticamente o layout."""
        # Implementar algoritmo de organização
        pass
```

## Próximos Passos
1. [ ] Implementar FlowEditor base
2. [ ] Desenvolver sistema de conexões
3. [ ] Criar gerador de diagramas
4. [ ] Implementar validações
5. [ ] Adicionar persistência de layout

## Dependências
- Mermaid.js
- Streamlit
- Componentes da Sprint 8
- Sistema de validação

## Riscos
1. Complexidade da interface
2. Performance com muitos passos
3. Bugs nas conexões
4. Problemas de layout
5. Experiência do usuário

## Estimativa
- Estrutura Base: 3 dias
- Editor Visual: 4 dias
- Geração Diagramas: 3 dias
- Validações: 2 dias
- Testes: 3 dias

Total: 3 semanas 