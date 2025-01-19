# Formulários do RPA Analyst

Este diretório contém os formulários modulares utilizados na aplicação RPA Analyst. Cada formulário é responsável por uma parte específica do processo de documentação.

## 1. Formulário de Identificação (IdentificationForm)

![Identificação do Processo](../../../docs/assets/images/identification_form.png)

### Objetivo
Coletar informações básicas de identificação do processo a ser automatizado.

### Campos
1. **Nome do Processo**
   - Tipo: Text Input
   - Obrigatório: Sim
   - Descrição: Nome que identifica unicamente o processo
   - Exemplo: "Processo de Onboarding de Funcionários"

2. **Responsável**
   - Tipo: Text Input
   - Obrigatório: Sim
   - Descrição: Pessoa responsável pelo processo
   - Exemplo: "João Silva"

3. **Descrição**
   - Tipo: Text Area
   - Obrigatório: Sim
   - Descrição: Descrição detalhada do processo em linguagem natural
   - Exemplo: "Processo que gerencia a entrada de novos funcionários..."

### Botões

1. **🎯 Formalizar Descrição**
   - Função: Aciona o agente de IA para formalizar a descrição informal
   - Comportamento:
     - Exibe preview da versão formalizada
     - Permite aprovação/edição da formalização
     - Mantém histórico de versões
     - Atualiza o campo de descrição após aprovação

2. **🤖 Gerar Sugestões**
   - Função: Infere dados para os próximos formulários
   - Comportamento:
     - Analisa a descrição do processo
     - Gera sugestões para:
       - Regras de negócio
       - Sistemas envolvidos
       - Objetivos de automação
       - Passos do processo
     - Exibe preview das sugestões
     - Permite aprovação/edição das sugestões

3. **✅ Salvar**
   - Função: Persiste os dados do formulário
   - Comportamento:
     - Valida campos obrigatórios
     - Salva dados no estado da aplicação
     - Avança para o próximo formulário
     - Exibe feedback de sucesso/erro

### Validações
- Nome do processo: não pode estar vazio
- Responsável: não pode estar vazio
- Descrição: mínimo de 50 caracteres

### Integração com IA
- Formalização de descrições informais
- Geração de sugestões para outros formulários
- Validação de consistência dos dados

### Fluxo de Uso
1. Usuário preenche os campos básicos
2. Pode formalizar a descrição se necessário
3. Pode gerar sugestões para agilizar o processo
4. Salva os dados e avança

### Exemplo de Uso
```python
# Inicialização do formulário
form = IdentificationForm()

# Renderização
await form.render()

# Formalização da descrição
if st.button("🎯 Formalizar"):
    formalized = await form.formalize_description()
    if st.button("✅ Aprovar Formalização"):
        form.update_description(formalized)

# Geração de sugestões
if st.button("🤖 Gerar Sugestões"):
    suggestions = await form.generate_suggestions()
    if st.button("✅ Aplicar Sugestões"):
        form.apply_suggestions(suggestions)
```

## 2. Outros Formulários (Em desenvolvimento)
- ProcessDetailsForm
- BusinessRulesForm
- AutomationGoalsForm
- SystemsForm
- DataForm
- StepsForm
- RisksForm
- DocumentationForm

## Arquitetura
- Todos os formulários herdam de `FormBase`
- Formulários com sugestões herdam de `SuggestibleForm`
- Integração com sistema de validação
- Gerenciamento de estado via `session_state`
- Suporte a operações assíncronas

## Boas Práticas
1. Manter validações consistentes
2. Implementar feedback visual claro
3. Garantir persistência dos dados
4. Documentar campos e comportamentos
5. Seguir padrões de UI/UX

## Próximos Passos
1. Implementar histórico de alterações
2. Adicionar mais validações
3. Melhorar feedback visual
4. Otimizar chamadas à IA
5. Implementar cache de sugestões 