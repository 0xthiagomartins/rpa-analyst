# Editor de Diagramas

## Visão Geral
O Editor de Diagramas é um componente central do sistema que permite a criação e edição visual de diagramas de processo. 

## Funcionalidades

### 1. Gerenciamento de Nós
- Criação de novos nós
- Edição de propriedades
- Exclusão de nós
- Tipos de nós suportados:
  - 🟢 Início
  - 🔷 Ação
  - 💠 Decisão
  - 🖥️ Sistema
  - 🔴 Fim

### 2. Gerenciamento de Conexões
- Criação de conexões entre nós
- Rótulos personalizados
- Validação de conexões
- Remoção automática de conexões órfãs

### 3. Sistema de Histórico
- Undo/Redo ilimitado
- Gerenciamento automático de memória
- Feedback visual do estado do histórico
- Persistência de estados

### 4. Interface
- Barra de ferramentas intuitiva
- Painel de propriedades contextual
- Feedback visual de ações
- Tooltips informativos
- Validação em tempo real

## Arquitetura

### Classes Principais
1. `DiagramState`
   - Representa um estado do diagrama
   - Gerencia nós e conexões
   - Suporta serialização

2. `DiagramEditor`
   - Implementa a interface visual
   - Gerencia interações do usuário
   - Mantém o histórico de estados

### Fluxo de Dados
1. Ações do usuário são capturadas
2. Estado é validado e atualizado
3. Histórico é mantido
4. Interface é atualizada
5. Feedback é fornecido

## Uso

### Inicialização
```python
from src.views.components.diagram_editor import DiagramEditor

editor = DiagramEditor()
editor.render_diagram_editor()
```

### Customização
```python
# Configurar tipos de nós personalizados
editor.NODE_TYPES = {
    'custom': {'label': '🔶 Custom', 'color': '#ff0000'}
}

# Ajustar limite do histórico
editor.MAX_HISTORY_SIZE = 50
```

## Boas Práticas
1. Sempre use o sistema de undo/redo para modificações
2. Valide o diagrama antes de salvar
3. Mantenha conexões significativas
4. Use rótulos descritivos
5. Organize o layout visualmente

## Limitações Conhecidas
1. Performance pode degradar com diagramas muito grandes
2. Algumas operações não podem ser desfeitas
3. Limite de memória para histórico 