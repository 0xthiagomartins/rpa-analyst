# Configurações do Processo 📝

## Overview
Este diretório contém as configurações e constantes utilizadas nos formulários do processo.

## Estrutura

### 1. Options (`options.py`)
Gerencia as opções e templates disponíveis nos formulários.

```python
from process.config.options import OPTIONS

# Exemplo de uso
tools = OPTIONS['common_tools']
data_types = OPTIONS['data_types']
```

#### Opções Disponíveis
- `common_tools`: Ferramentas e sistemas comuns
- `data_types`: Tipos de dados processados
- `data_formats`: Formatos de arquivo suportados
- `data_sources`: Fontes de dados
- `business_rules_templates`: Templates de regras de negócio
- `common_exceptions`: Exceções comuns
- `automation_goals`: Objetivos de automação
- `kpi_templates`: Templates de KPIs

### 2. Constantes (`constants.py`)
Define constantes e configurações estáticas do sistema.

```python
from process.config.constants import FORM_STATES, STEP_TYPES, ERROR_MESSAGES, UI_CONFIG

# Exemplo de uso
if state == FORM_STATES['EDITING']:
    ...

if step_type == STEP_TYPES['ACTION']:
    ...
```

#### Grupos de Constantes
- `FORM_STATES`: Estados possíveis do formulário
- `STEP_TYPES`: Tipos de etapas do processo
- `ERROR_MESSAGES`: Mensagens de erro padronizadas
- `UI_CONFIG`: Configurações de interface

## Configuração via YAML

As opções podem ser customizadas através do arquivo `config/form_options.yaml`:

```yaml
common_tools:
  - Microsoft Excel
  - Microsoft Outlook
  # ...

data_types:
  - Dados financeiros
  - Documentos fiscais
  # ...
```

### Carregamento de Configurações
1. O sistema tenta carregar as configurações do YAML
2. Se falhar, usa as opções padrão de `get_default_options()`
3. Verifica se todas as chaves necessárias existem
4. Preenche chaves faltantes com valores padrão

## Uso em Formulários

```python
from process.config.options import OPTIONS
from process.config.constants import UI_CONFIG

def render_form():
    # Usando opções
    tools = st.multiselect(
        "Ferramentas:",
        OPTIONS['common_tools']
    )
    
    # Usando configurações de UI
    description = st.text_area(
        "Descrição:",
        height=UI_CONFIG['DEFAULT_HEIGHT']
    )
```

## Extensão e Customização

Para adicionar novas opções:
1. Atualize `form_options.yaml`
2. Adicione valores padrão em `get_default_options()`
3. Atualize a documentação se necessário

## Boas Práticas
1. Sempre use as constantes ao invés de strings literais
2. Mantenha o YAML e os valores padrão sincronizados
3. Documente novas opções e constantes
4. Use tipos consistentes (strings, listas, etc) 