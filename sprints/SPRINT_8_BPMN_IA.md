# Sprint 8 - Geração de BPMN e Sugestões IA

## Objetivo
Implementar a geração automática de BPMN a partir dos dados coletados e adicionar sugestões inteligentes baseadas na descrição inicial do processo.

## Status Atual
🟡 Não Iniciado (0%)

## Análise de Requisitos para BPMN

### Dados Necessários Adicionais
1. **Fluxo de Processo**
   - [x] Passos sequenciais (já temos)
   - [x] Pontos de decisão (já temos)
   - [x] Loops (já temos)
   - [ ] Eventos de início/fim (precisamos adicionar)
   - [ ] Gateways paralelos (precisamos adicionar)
   - [ ] Tipos de tarefas (manual, automática, usuário)
   - [ ] Conexões entre sistemas (precisamos estruturar melhor)

2. **Atores e Raias**
   - [x] Responsáveis por cada passo (já temos)
   - [ ] Departamentos/Áreas envolvidas
   - [ ] Hierarquia de responsabilidades

## Fases de Implementação

### Fase 1: Ajustes nos Formulários
1. **StepsForm Aprimorado**
   - [ ] Adicionar tipos de tarefas
   - [ ] Incluir eventos de início/fim
   - [ ] Adicionar gateways paralelos
   - [ ] Melhorar estrutura de conexões

2. **Novo OrganizationalForm**
   - [ ] Estrutura organizacional
   - [ ] Departamentos
   - [ ] Hierarquia
   - [ ] Responsabilidades

### Fase 2: Integração com IA
1. **Atualização do AIService**
   - [ ] Refatorar para novo modelo de formulários
   - [ ] Adicionar suporte a processamento em lote
   - [ ] Implementar cache de respostas
   - [ ] Melhorar tratamento de erros
   - [ ] Adicionar logging detalhado
   - [ ] Implementar rate limiting

2. **Sugestões Automáticas**
   - [ ] Implementar botão "Sugerir Melhorias" no IdentificationForm
   - [ ] Desenvolver prompt de engenharia para IA
   - [ ] Implementar parser para respostas da IA
   - [ ] Desenvolver preview de sugestões
   - [ ] Implementar aplicação de sugestões

3. **Geração de BPMN**
   - [ ] Desenvolver conversor de dados para formato BPMN
   - [ ] Implementar geração de código Mermaid
   - [ ] Criar visualizador de BPMN
   - [ ] Adicionar exportação do diagrama

### Fase 3: Validação e Testes
1. **Testes Automatizados**
   - [ ] Testes unitários para novos componentes
   - [ ] Testes de integração com IA
   - [ ] Testes de geração BPMN

2. **Validação de Qualidade**
   - [ ] Validar qualidade das sugestões
   - [ ] Verificar conformidade do BPMN
   - [ ] Testar diferentes cenários

## Componentes a Serem Desenvolvidos/Atualizados

1. **AIService Aprimorado**
   ```python
   class AIService:
       """Serviço de comunicação com IA."""
       
       def __init__(self, config: Dict):
           """Inicializa com configurações."""
           self.config = config
           self.cache = Cache()
           self.rate_limiter = RateLimiter()
           self.logger = Logger()
       
       async def suggest_improvements(self, description: str) -> Dict[str, Any]:
           """Sugere melhorias e gera dados estruturados para todos os formulários."""
           try:
               cached = self.cache.get(description)
               if cached:
                   return cached
               
               await self.rate_limiter.acquire()
               response = await self._process_suggestions(description)
               
               self.cache.set(description, response)
               return response
               
           except Exception as e:
               self.logger.error(f"Erro ao processar sugestões: {str(e)}")
               raise
       
       async def generate_bpmn(self, process_data: Dict) -> str:
           """Gera código Mermaid para BPMN."""
           
       async def _process_suggestions(self, description: str) -> Dict[str, Any]:
           """Processa o texto e retorna sugestões estruturadas."""
           return {
               "identification": {...},
               "organization": {...},
               "steps": {...},
               "systems": {...},
               "data": {...},
               "rules": {...},
               "goals": {...},
               "risks": {...},
               "documentation": {...}
           }
   ```

2. **Componentes de Suporte**
   ```python
   class Cache:
       """Cache para respostas da IA."""
       
   class RateLimiter:
       """Limitador de taxa para chamadas à API."""
       
   class AIResponseParser:
       """Parser para respostas da IA."""
   ```

3. **Geradores BPMN**
   ```python
   class BPMNGenerator:
       """Gerador de diagramas BPMN."""
       def convert_to_mermaid(self, process_data: Dict) -> str
   ```

## Próximos Passos Imediatos
1. [ ] Definir estrutura detalhada do BPMN
2. [ ] Atualizar AIService para novo modelo
3. [ ] Implementar OrganizationalForm
4. [ ] Atualizar StepsForm
5. [ ] Desenvolver integração com IA
6. [ ] Implementar geração de BPMN

## Dependências
- OpenAI API ou similar para IA
- Biblioteca Mermaid.js para renderização
- Componentes atuais do sistema
- Redis ou similar para cache
- Sistema de logging aprimorado

## Riscos
1. Qualidade das sugestões da IA
2. Complexidade na geração do BPMN
3. Performance com processos grandes
4. Custo das chamadas à API de IA
5. Limites de taxa da API
6. Consistência do cache

## Estimativa de Tempo
- Ajustes nos Formulários: 1 semana
- Atualização do AIService: 1 semana
- Integração com IA: 1 semana
- Geração BPMN: 2 semanas
- Testes e Validação: 1 semana

Total: 6 semanas 