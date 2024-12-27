# Agente Analista de RPA 🤖

Uma aplicação web para auxiliar analistas de RPA na criação de documentos PDD (Process Definition Document) de forma inteligente e eficiente.

## 🎯 Funcionalidades

- **Formulários Inteligentes**
  - Identificação do Processo
  - Detalhes do Processo
  - Regras de Negócio
  - Objetivos da Automação

- **Geração de Diagramas**
  - Geração automática via IA
  - Editor visual de diagramas Mermaid
  - Preview em tempo real
  - Explicações detalhadas do fluxo

- **Documentação**
  - Geração de PDDs em PDF
  - Layout profissional e padronizado
  - Exportação automática

## 🚀 Começando

### Pré-requisitos

- Python 3.10+
- pip (gerenciador de pacotes Python)
- Chave de API da OpenAI

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/analyst.git
cd analyst
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com sua chave da OpenAI
```

### Executando

```bash
python src/run.py
```

A aplicação estará disponível em `http://localhost:8501`

## 🧪 Testes

Execute os testes com:
```bash
pytest
```

Para ver a cobertura de testes:
```bash
pytest --cov=src
```

## 🏗️ Arquitetura

A aplicação segue uma arquitetura em camadas:

- **Views**: Interface do usuário usando Streamlit
- **Services**: Lógica de negócios e integração com IA
- **Models**: Estruturas de dados e validações
- **Templates**: Templates para geração de documentos

Para mais detalhes, consulte [DIAGRAMS.md](DIAGRAMS.md)

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) - Framework web
- [LangChain](https://langchain.com/) - Framework de IA
- [OpenAI GPT](https://openai.com/) - Modelo de linguagem
- [Mermaid](https://mermaid.js.org/) - Diagramas
- [ReportLab](https://www.reportlab.com/) - Geração de PDFs

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📋 Roadmap

- [x] Estrutura básica da aplicação
- [x] Formulários de entrada
- [x] Integração com OpenAI
- [x] Geração de diagramas
- [x] Geração de PDDs
- [ ] Persistência de dados
- [ ] Customização de templates
- [ ] Exportação em múltiplos formatos
- [ ] Interface de administração
- [x] Assistente de Formalização
  - [x] Botão "Formalizar" para descrições informais
  - [x] Preview da versão formalizada
  - [x] Sistema de aprovação/edição da formalização
  - [x] Histórico de versões da descrição
- [ ] Auto-preenchimento Inteligente
  - [ ] Inferência de sistemas e ferramentas a partir da descrição
  - [ ] Sugestão de regras de negócio baseadas no contexto
  - [ ] Identificação automática de objetivos de automação
  - [ ] Sistema de feedback para validação das sugestões
  - [ ] Aprendizado contínuo com base nos feedbacks dos usuários
- [ ] Sistema de Precificação
  - [ ] Análise de complexidade baseada em:
    - [ ] Número de sistemas envolvidos
    - [ ] Volume de dados processados
    - [ ] Quantidade de regras de negócio
    - [ ] Número de exceções a tratar
    - [ ] Complexidade das integrações
  - [ ] Cálculo de esforço:
    - [ ] Estimativa de horas de desenvolvimento
    - [ ] Necessidade de infraestrutura
    - [ ] Licenças de software necessárias
  - [ ] Fatores de ajuste:
    - [ ] Criticidade do processo
    - [ ] Nível de segurança requerido
    - [ ] Complexidade das validações
    - [ ] Necessidade de manutenção
  - [ ] Dashboard de custos:
    - [ ] Breakdown dos custos por categoria
    - [ ] ROI estimado
    - [ ] Payback period
    - [ ] Comparativo com processo manual

## 🧠 Auto-preenchimento Inteligente (Planejado)

### Visão Geral
O sistema utilizará IA para analisar a descrição inicial do processo e pré-preencher 
automaticamente diversos campos dos formulários subsequentes:

1. **Análise da Descrição**
  - Processamento de linguagem natural da descrição do processo
  - Identificação de entidades e conceitos-chave
  - Extração de relacionamentos e dependências

2. **Campos Auto-preenchidos**
  - Sistemas e Ferramentas envolvidos
  - Regras de Negócio implícitas
  - Objetivos potenciais da automação
  - KPIs sugeridos

3. **Sistema de Validação**
  - Interface de confirmação para cada sugestão
  - Possibilidade de edição e ajuste
  - Feedback para melhorar sugestões futuras

4. **Benefícios**
  - Redução do tempo de preenchimento
  - Maior consistência nas informações
  - Captura de detalhes que poderiam ser esquecidos
  - Aprendizado contínuo com base no uso

## 📝 Assistente de Formalização (Planejado)

### Visão Geral
O sistema oferecerá um assistente para transformar descrições informais em documentação 
técnica profissional:

1. **Processo de Formalização**
  - Análise do texto informal
  - Identificação de termos técnicos relevantes
  - Estruturação em formato profissional
  - Padronização da linguagem

2. **Interface do Usuário**
  - Campo de texto para descrição informal
  - Botão "Formalizar" de fácil acesso
  - Preview lado a lado (informal vs formal)
  - Opções de personalização do nível de formalidade

3. **Sistema de Aprovação**
  - Visualização das alterações sugeridas
  - Opção de aceitar/rejeitar mudanças específicas
  - Editor para ajustes finos
  - Confirmação final antes da atualização

4. **Benefícios**
  - Documentação mais profissional
  - Consistência na linguagem técnica
  - Economia de tempo na redação
  - Melhoria na qualidade da documentação

5. **Recursos Adicionais**
  - Histórico de versões da descrição
  - Sugestões de melhorias incrementais
  - Integração com glossário técnico
  - Adaptação ao estilo da organização

## 👥 Autores

* **Thiago Martins** - *Trabalho inicial* - [@0xthiagomartins](https://github.com/0xthiagomartins)

## 🙏 Agradecimentos

* OpenAI pela API do GPT
* Comunidade Streamlit
* Contribuidores do projeto
