# Agente Analista de RPA

Um aplicativo Streamlit para auxiliar na criação de documentos PDD (Process Definition Document) para automação RPA.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/agente-analista-rpa.git
cd agente-analista-rpa
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o aplicativo com:
```bash
streamlit run src/app.py
```

## Testes

Para executar os testes:

```bash
# Executa todos os testes com relatório de cobertura
pytest

# Executa testes com saída detalhada
pytest -v

# Executa testes de um módulo específico
pytest tests/test_models/test_process.py

# Gera relatório de cobertura em HTML
pytest --cov=src --cov-report=html
```

O relatório de cobertura HTML será gerado em `htmlcov/index.html`

## Estrutura do Projeto

- `src/`: Código fonte do aplicativo
  - `controllers/`: Controladores da aplicação
  - `models/`: Modelos de dados
  - `views/`: Componentes da interface
  - `utils/`: Utilitários e helpers
- `tests/`: Testes automatizados
  - `conftest.py`: Configurações e fixtures do pytest
  - `test_models/`: Testes dos modelos
  - `test_controllers/`: Testes dos controladores
  - `test_utils/`: Testes dos utilitários
- `templates/`: Templates para geração de documentos
- `config/`: Arquivos de configuração

## Desenvolvimento

Para contribuir com o projeto:

1. Crie uma branch para sua feature
2. Adicione testes para novas funcionalidades
3. Garanta que todos os testes passem
4. Envie um Pull Request

## Mapa de Desenvolvimento

1. Fase A - Reestruturação do Projeto ✅
   - Reorganizar a estrutura de arquivos
   - Implementar padrão MVC
   - Criar documentação básica
   - Adicionar logging

2. Fase B - Melhorias na Interface ✅
   - Adicionar validação de campos
   - Melhorar feedback visual
   - Implementar navegação entre seções
   - Adicionar progress tracking

3. Fase C - Lógica de Negócios
   - Implementar classes para gerenciamento de dados
   - Adicionar validações de regras de negócio
   - Criar templates customizáveis para o PDD
   - Implementar versionamento de documentos

4. Fase D - Persistência e Exportação
   - Adicionar banco de dados
   - Implementar exportação para diferentes formatos (PDF, DOCX)
   - Adicionar sistema de templates

5. Fase E - Qualidade e Testes ✅
   - Implementar testes unitários
   - Adicionar testes de integração
   - Implementar CI/CD
   - Adicionar análise de código

## Licença

MIT
