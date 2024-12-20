# Agente Analista de RPA

Sistema para geração assistida de documentos PDD (Process Definition Document) para automação RPA.

## 🚀 Funcionalidades

- ✅ Criação guiada de PDDs
- ✅ Validação de dados em tempo real
- ✅ Geração de documentos em HTML e PDF
- ✅ Interface intuitiva com múltiplas etapas
- ✅ Sistema de templates customizável

## 🛠️ Tecnologias

- Python 3.8+
- Streamlit
- Jinja2
- PDFKit
- PyYAML
- Pytest

## 📋 Pré-requisitos

1. Python 3.8 ou superior
2. wkhtmltopdf instalado no sistema
3. Pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/analyst.git
cd analyst
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o wkhtmltopdf:
- Windows: Baixe e instale de https://wkhtmltopdf.org/downloads.html
- Linux: `sudo apt-get install wkhtmltopdf`
- Mac: `brew install wkhtmltopdf`

## 🚀 Uso

1. Inicie a aplicação:
```bash
python src/run.py
```

2. Acesse no navegador:
```
http://localhost:8501
```

## 🧪 Testes

Execute os testes com:
```bash
pytest
```

Para relatório de cobertura:
```bash
pytest --cov=src
```

## 📁 Estrutura do Projeto

```
analyst/
├── config/             # Configurações
├── src/               # Código fonte
│   ├── controllers/   # Controladores
│   ├── models/        # Modelos
│   ├── services/      # Serviços
│   ├── templates/     # Templates
│   ├── utils/         # Utilitários
│   └── views/         # Componentes da interface
├── tests/             # Testes
└── output/            # PDDs gerados
```

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
