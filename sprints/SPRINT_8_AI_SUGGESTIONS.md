# Sprint 8 - Sugestões IA e Melhorias Automáticas

## Objetivo
Implementar sistema de sugestões automáticas usando IA para melhorar a descrição do processo e auto-preencher formulários subsequentes.

## Status Atual
🟡 Em Andamento (75%)

### Concluído
1. ✅ Cache em memória (InMemoryCache)
2. ✅ AIService com testes
3. ✅ Tipos de dados (ai_types.py)
4. ✅ Sistema de prompts básico
5. ✅ IdentificationForm com sugestões
6. ✅ SuggestionButton
7. ✅ Buffer de sugestões no session_state
8. ✅ Controle de estado das sugestões
9. ✅ Preview contextual por formulário

### Em Andamento
1. 🟡 Implementar preview nos outros formulários
2. 🟡 Sistema de distribuição de dados
3. 🟡 Aplicação seletiva de sugestões

### Próximos Passos
1. Implementar preview nos formulários:
   - [✓] ProcessDetailsForm
   - [✓] BusinessRulesForm
   - [✓] AutomationGoalsForm
   - [ ] SystemsForm
   - [ ] DataForm
   - [ ] StepsForm
   - [ ] RisksForm
   - [ ] DocumentationForm

2. Melhorias no sistema de sugestões:
   - [ ] Validação de dados antes da aplicação
   - [ ] Preview de mudanças
   - [ ] Histórico de sugestões
   - [ ] Rollback de mudanças

## Fases de Implementação

### Fase 1: Atualização do AIService
1. **Refatoração do Serviço**
   - [x] Implementar cache em memória
   - [x] Adaptar para novo modelo de formulários
   - [x] Adicionar logging detalhado
   - [x] Melhorar tratamento de erros

2. **Sistema de Prompts**
   - [x] Desenvolver prompts de engenharia
   - [x] Criar templates de resposta
   - [x] Implementar validação de respostas
   - [ ] Adicionar exemplos de treinamento

3. **Testes**
   - [x] Testes do cache
   - [x] Testes do AIService
   - [x] Testes do SuggestionsManager
   - [ ] Testes de integração
   - [ ] Testes de carga

### Fase 2: Parser de Respostas
1. **Estrutura de Dados**
   - [x] Definir tipos de dados
   - [x] Implementar validações
   - [x] Criar interfaces

2. **Implementação**
   - [x] Criar parser de respostas da IA
   - [x] Implementar mapeamento para formulários
   - [x] Adicionar validação de dados
   - [x] Criar preview de sugestões

3. **Testes**
   - [x] Testes do cache
   - [x] Testes do AIService
   - [x] Testes do SuggestionsManager
   - [ ] Testes de integração
   - [ ] Testes de carga

### Fase 3: Integração com Formulários
1. **IdentificationForm**
   - [x] Adicionar botão "Sugerir Melhorias"
   - [x] Implementar preview de sugestões
   - [x] Criar interface de confirmação
   - [x] Adicionar feedback visual

2. **Auto-preenchimento**
   - [ ] Implementar distribuição de dados
   - [ ] Criar buffer de sugestões
   - [ ] Adicionar preview em outros forms
   - [ ] Implementar aplicação seletiva

## Componentes Principais

### 1. Cache em Memória
```python
from typing import Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict

class InMemoryCache:
    """Cache em memória com interface similar ao Redis."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, tuple[Any, datetime]] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache."""
        if key not in self.cache:
            return None
            
        value, expiry = self.cache[key]
        if expiry < datetime.now():
            del self.cache[key]
            return None
            
        # Move para o fim (LRU)
        self.cache.move_to_end(key)
        return value
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> None:
        """Adiciona valor ao cache."""
        # Remove item mais antigo se necessário
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        expiry = (
            datetime.now() + timedelta(seconds=ttl)
            if ttl
            else datetime.max
        )
        
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Remove valor do cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
```

### 2. AIService Atualizado
```python
class AIService:
    """Serviço de comunicação com IA."""
    
    def __init__(self):
        self.cache = InMemoryCache()
        self.logger = Logger()
    
    async def suggest_improvements(
        self, 
        description: str,
        current_data: Optional[Dict] = None
    ) -> AIResponse:
        """Sugere melhorias e gera dados estruturados."""
        try:
            # Verifica cache
            cached = self.cache.get(description)
            if cached:
                return cached
            
            # Gera prompt
            prompt = self._generate_prompt(description, current_data)
            
            # Processa com IA
            response = await self._process_with_ai(prompt)
            
            # Valida e parseia resposta
            parsed = self._parse_response(response)
            
            # Atualiza cache (24h)
            self.cache.set(description, parsed, ttl=86400)
            
            return parsed
            
        except Exception as e:
            self.logger.error(f"Erro ao processar sugestões: {str(e)}")
            raise
```

### 2. SuggestionsManager
```python
class SuggestionsManager:
    """Gerenciador de sugestões da IA."""
    
    def __init__(self):
        self.ai_service = AIService()
        self.parser = AIResponseParser()
    
    def preview_suggestions(
        self, 
        suggestions: AIResponse
    ) -> None:
        """Mostra preview das sugestões."""
        st.write("### Sugestões de Melhoria")
        
        # Descrição melhorada
        with st.expander("✍️ Descrição Formal", expanded=True):
            st.write(suggestions.description)
            if st.button("Aplicar"):
                self._apply_description(suggestions.description)
        
        # Dados para outros formulários
        with st.expander("📝 Dados Sugeridos"):
            for form_id, data in suggestions.forms_data.items():
                st.write(f"**{form_id}**")
                st.json(data)
    
    def apply_suggestions(
        self, 
        suggestions: AIResponse,
        selected_forms: List[str]
    ) -> None:
        """Aplica sugestões selecionadas."""
        for form_id in selected_forms:
            if form_id in suggestions.forms_data:
                self._apply_to_form(
                    form_id, 
                    suggestions.forms_data[form_id]
                )
```

## Próximos Passos
1. [ ] Atualizar AIService
2. [ ] Implementar sistema de prompts
3. [ ] Desenvolver parser de respostas
4. [ ] Integrar com IdentificationForm
5. [ ] Implementar preview de sugestões

## Dependências
- OpenAI API
- Sistema de logging
- Componentes atuais

## Riscos
1. Qualidade das sugestões da IA
2. Custo das chamadas à API
3. Performance do cache em memória
4. Complexidade do parser
5. Usabilidade do preview

## Estimativa
- Atualização AIService: 3 dias
- Sistema de Prompts: 2 dias
- Parser de Respostas: 3 dias
- Integração Forms: 2 dias
- Testes: 2 dias

Total: 2 semanas 

## Especificações Técnicas

### 1. Estrutura de Prompts

```python
SYSTEM_PROMPT = """
Você é um assistente especializado em análise e documentação de processos. 
Seu objetivo é analisar descrições de processos e:
1. Formalizar a descrição
2. Identificar elementos estruturais
3. Sugerir melhorias
4. Gerar dados estruturados para documentação

Siga estritamente o formato de resposta especificado.
"""

USER_PROMPT_TEMPLATE = """
Analise a seguinte descrição de processo:

{description}

Formate sua resposta como JSON com:
1. Descrição formal e estruturada
2. Dados para cada formulário do processo
3. Sugestões de melhoria
4. Validações e avisos

Formulários disponíveis:
- identification (nome, responsável, área)
- steps (passos, sequência, responsáveis)
- systems (sistemas, integrações)
- data (entradas, saídas)
- rules (regras de negócio)
- goals (objetivos, KPIs)
- risks (riscos, mitigações)
- documentation (docs, referências)
"""

EXAMPLE_RESPONSE = {
    "description": "Processo estruturado de análise...",
    "forms_data": {
        "identification": {
            "name": "Análise de Crédito",
            "responsible": "Departamento Financeiro",
            "area": "Financeiro"
        },
        "steps": [
            {
                "sequence": 1,
                "description": "Receber solicitação",
                "responsible": "Atendente",
                "type": "start"
            }
        ]
        # ... outros formulários
    },
    "suggestions": [
        "Adicionar validação de dados no início",
        "Incluir notificação automática"
    ],
    "validation": [
        "Processo precisa de ponto de decisão",
        "Falta definição de SLA"
    ]
}
```

### 2. Estratégia de Cache

```python
from typing import Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict

class InMemoryCache:
    """Cache em memória com interface similar ao Redis."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, tuple[Any, datetime]] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache."""
        if key not in self.cache:
            return None
            
        value, expiry = self.cache[key]
        if expiry < datetime.now():
            del self.cache[key]
            return None
            
        # Move para o fim (LRU)
        self.cache.move_to_end(key)
        return value
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> None:
        """Adiciona valor ao cache."""
        # Remove item mais antigo se necessário
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        expiry = (
            datetime.now() + timedelta(seconds=ttl)
            if ttl
            else datetime.max
        )
        
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Remove valor do cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
```

### 3. Estrutura de Dados

```python
from typing import TypedDict, List, Optional, Literal

class FormData(TypedDict):
    """Dados base para formulários."""
    form_id: str
    is_valid: bool
    has_changes: bool
    data: dict

class AIResponse(TypedDict):
    """Resposta da IA."""
    description: str
    forms_data: dict[str, FormData]
    suggestions: List[str]
    validation: List[str]

class SuggestionPreview(TypedDict):
    """Preview de sugestões."""
    original: str
    improved: str
    changes: List[str]
    confidence: float
    form_previews: dict[str, FormPreview]

class FormPreview(TypedDict):
    """Preview de mudanças no formulário."""
    form_id: str
    changes: List[Change]
    validation: List[str]

class Change(TypedDict):
    """Mudança sugerida."""
    field: str
    old_value: Optional[str]
    new_value: str
    type: Literal['add', 'modify', 'remove']
    confidence: float
```

### 4. Interface do Preview

```python
class SuggestionsPreview:
    """Componente de preview de sugestões."""
    
    def render(self, suggestions: AIResponse):
        """Renderiza interface de preview."""
        st.write("### 📝 Sugestões de Melhoria")
        
        # Descrição
        with st.expander("✨ Descrição Melhorada", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Original:**")
                st.text(suggestions.original)
            with col2:
                st.write("**Sugerido:**")
                st.text(suggestions.improved)
                
            if st.button("Aplicar Melhoria"):
                self._apply_description(suggestions.improved)
        
        # Formulários
        with st.expander("📋 Sugestões para Formulários"):
            tabs = st.tabs([
                form.title() for form 
                in suggestions.forms_data.keys()
            ])
            
            for tab, (form_id, data) in zip(
                tabs, 
                suggestions.forms_data.items()
            ):
                with tab:
                    self._render_form_preview(form_id, data)
        
        # Ações
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Aplicar Selecionados"):
                self._apply_selected(suggestions)
        with col2:
            if st.button("❌ Descartar"):
                self._discard_suggestions()
    
    def _render_form_preview(
        self, 
        form_id: str, 
        data: FormPreview
    ):
        """Renderiza preview de um formulário."""
        for change in data.changes:
            st.checkbox(
                f"{change.type.title()}: {change.field}",
                value=False,
                key=f"change_{form_id}_{change.field}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.text("Atual: " + str(change.old_value))
            with col2:
                st.text("Sugerido: " + str(change.new_value))
```

### 5. Fluxo de Validação

1. **Pré-validação**
   - Verificar formato da descrição
   - Validar tamanho e complexidade
   - Checar conteúdo inadequado

2. **Validação da Resposta da IA**
   - Verificar estrutura JSON
   - Validar campos obrigatórios
   - Checar tipos de dados
   - Validar referências entre formulários

3. **Validação de Aplicação**
   - Verificar consistência dos dados
   - Validar regras de negócio
   - Checar impacto das mudanças
   - Validar integridade do processo 