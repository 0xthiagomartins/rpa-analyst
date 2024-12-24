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

## 👥 Autores

* **Seu Nome** - *Trabalho inicial* - [seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

* OpenAI pela API do GPT
* Comunidade Streamlit
* Contribuidores do projeto
