# Sprint 8 - Sugestões IA e Melhorias Automáticas

## Objetivo
Implementar sistema de sugestões automáticas usando IA para melhorar a descrição do processo e auto-preencher formulários subsequentes.

## Status Atual
🟡 Não Iniciado (0%)

## Fases de Implementação

### Fase 1: Atualização do AIService
1. **Refatoração do Serviço**
   - [ ] Adaptar para novo modelo de formulários
   - [ ] Implementar cache de respostas
   - [ ] Adicionar logging detalhado
   - [ ] Implementar rate limiting
   - [ ] Melhorar tratamento de erros

2. **Sistema de Prompts**
   - [ ] Desenvolver prompts de engenharia
   - [ ] Criar templates de resposta
   - [ ] Implementar validação de respostas
   - [ ] Adicionar exemplos de treinamento

### Fase 2: Parser de Respostas
1. **Estrutura de Dados**
   ```python
   class AIResponse(TypedDict):
       description: str
       forms_data: Dict[str, Any]
       suggestions: List[str]
       validation: List[str]
   ```

2. **Implementação**
   - [ ] Criar parser de respostas da IA
   - [ ] Implementar mapeamento para formulários
   - [ ] Adicionar validação de dados
   - [ ] Criar preview de sugestões

### Fase 3: Integração com Formulários
1. **IdentificationForm**
   - [ ] Adicionar botão "Sugerir Melhorias"
   - [ ] Implementar preview de sugestões
   - [ ] Criar interface de confirmação
   - [ ] Adicionar feedback visual

2. **Auto-preenchimento**
   - [ ] Implementar distribuição de dados
   - [ ] Criar buffer de sugestões
   - [ ] Adicionar preview em outros forms
   - [ ] Implementar aplicação seletiva

## Componentes Principais

### 1. AIService Atualizado
```python
class AIService:
    """Serviço de comunicação com IA."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.cache = Cache()
        self.logger = Logger()
        self.rate_limiter = RateLimiter()
    
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
            
            # Rate limiting
            await self.rate_limiter.acquire()
            
            # Gera prompt
            prompt = self._generate_prompt(description, current_data)
            
            # Processa com IA
            response = await self._process_with_ai(prompt)
            
            # Valida e parseia resposta
            parsed = self._parse_response(response)
            
            # Atualiza cache
            self.cache.set(description, parsed)
            
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
- Redis para cache
- Sistema de logging
- Componentes atuais

## Riscos
1. Qualidade das sugestões da IA
2. Custo das chamadas à API
3. Performance do cache
4. Complexidade do parser
5. Usabilidade do preview

## Estimativa
- Atualização AIService: 3 dias
- Sistema de Prompts: 2 dias
- Parser de Respostas: 3 dias
- Integração Forms: 2 dias
- Testes: 2 dias

Total: 2 semanas 