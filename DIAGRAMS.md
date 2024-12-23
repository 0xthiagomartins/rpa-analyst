# Diagramas do Sistema

## 1. Visão Geral da Arquitetura

```mermaid
graph TD
    UI[Interface do Usuário - Streamlit] --> Forms[Formulários do PDD]
    UI --> DiagramEditor[Editor de Diagramas]
    Forms --> AIService[Serviço de IA]
    Forms --> DocumentService[Serviço de Documentos]
    DiagramEditor --> AIService
    AIService --> OpenAI[OpenAI/GPT]
    DocumentService --> Templates[Templates HTML]
    DocumentService --> PDFGenerator[Gerador PDF - WeasyPrint]
```

## 2. Fluxo do Usuário

```mermaid
flowchart TD
    Start[Início] --> Step1[1. Identificação do Processo]
    Step1 --> Step2[2. Detalhes do Processo]
    Step2 --> Step3[3. Regras de Negócio]
    Step3 --> Step4[4. Objetivos da Automação]
    Step4 --> GenerateDiagram[Gerar Diagrama com IA]
    GenerateDiagram --> EditDiagram[Editar Diagrama]
    EditDiagram --> GeneratePDD[Gerar PDD]
    GeneratePDD --> Download[Download do Documento]
```

## 3. Estrutura de Componentes

```mermaid
classDiagram
    class App {
        +init_session_state()
        +render_navigation()
        +render_current_step()
        +main()
    }
    
    class AIService {
        +generate_diagram()
    }
    
    class DocumentService {
        +generate_pdd()
        -validate_data()
        -create_template_env()
    }
    
    class DiagramEditor {
        +render_diagram_editor()
    }
    
    class ProcessForms {
        +render_process_identification()
        +render_process_details()
        +render_business_rules()
        +render_automation_goals()
    }
    
    App --> ProcessForms
    App --> DiagramEditor
    DiagramEditor --> AIService
    App --> DocumentService
```

## 4. Fluxo de Dados

```mermaid
flowchart LR
    subgraph Entrada
        Forms[Formulários]
        Steps[Passos do Processo]
    end
    
    subgraph Processamento
        AI[Serviço IA]
        Templates[Templates]
        Validation[Validação]
    end
    
    subgraph Saída
        Diagram[Diagrama Mermaid]
        PDF[Documento PDF]
    end
    
    Forms --> Validation
    Steps --> AI
    AI --> Diagram
    Forms --> Templates
    Templates --> PDF
    Validation --> PDF
```

## 5. Ciclo de Vida do PDD

```mermaid
stateDiagram-v2
    [*] --> Identificação
    Identificação --> Detalhes
    Detalhes --> Regras
    Regras --> Objetivos
    Objetivos --> Diagrama
    Diagrama --> Revisão
    Revisão --> Documento
    Documento --> [*]
    
    Revisão --> Diagrama: Ajustes
    Documento --> Revisão: Correções
```

## Notas Técnicas

1. **Interface**: Streamlit para interface web interativa
2. **IA**: Integração com OpenAI/GPT para geração de diagramas
3. **Documentação**: 
   - Templates HTML com Jinja2
   - Geração PDF com WeasyPrint
4. **Armazenamento**: Sistema de arquivos local para PDDs gerados
5. **Visualização**: Mermaid.js para renderização de diagramas

## Próximas Melhorias

1. Persistência de dados
2. Exportação em diferentes formatos
3. Integração com sistemas externos
4. Versionamento de documentos
5. Customização de templates 