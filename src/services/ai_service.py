from dataclasses import dataclass
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class MermaidDiagram:
    """Classe para armazenar o diagrama e sua explicação."""
    diagram_code: str
    explanation: str

class AIService:
    """Serviço para geração de conteúdo usando IA."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
    
    def generate_diagram(self, process_description: str, steps: List[str]) -> MermaidDiagram:
        """Gera um diagrama Mermaid baseado na descrição do processo e seus passos."""
        # Validação mais rigorosa dos inputs
        if not process_description or not isinstance(process_description, str):
            raise ValueError("Descrição do processo e passos são obrigatórios")
        if not steps or not isinstance(steps, list) or not all(steps):
            raise ValueError("Descrição do processo e passos são obrigatórios")
            
            # Template do prompt
        template = """
        Você é um especialista em criar diagramas de fluxo usando Mermaid.
        Crie um diagrama de fluxo que represente o processo descrito abaixo.
        Use a sintaxe flowchart TD do Mermaid.
            
            Descrição do Processo:
            {description}
            
            Passos do Processo:
            {steps}
            
        Regras para o diagrama:
        1. Use flowchart TD (top-down)
        2. Identifique cada nó com IDs únicos (p1, p2, etc)
        3. Use formas apropriadas para diferentes tipos de ações
        4. Conecte os nós de forma lógica
        5. Mantenha o texto em português
        6. Mantenha o diagrama limpo e legível
        
        Retorne apenas:
        1. O código Mermaid do diagrama
        2. Uma breve explicação do fluxo
        
        Formato da resposta:
        ```mermaid
        [código do diagrama aqui]
        ```
        
        Explicação:
        [explicação aqui]
        """
        
        # Prepara o prompt
        prompt = ChatPromptTemplate.from_template(template)
    
        # Prepara os dados
        formatted_steps = "\n".join(f"- {step}" for step in steps)
        
        # Cria e executa a chain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = chain.invoke({
            "description": process_description,
            "steps": formatted_steps
        })
        
        # Processa a resposta
        response = result['text']
        
        # Extrai o código do diagrama
        diagram_start = response.find("```mermaid")
        if diagram_start == -1:
            raise ValueError("Não foi possível extrair o diagrama da resposta")
            
        diagram_end = response.find("```", diagram_start + 10)
        diagram_code = response[diagram_start + 10:diagram_end].strip()
        
        # Extrai a explicação
        explanation_start = response.find("Explicação:")
        if explanation_start == -1:
            explanation = "Sem explicação disponível"
        else:
            explanation = response[explanation_start + 11:].strip()
        
        return MermaidDiagram(
            diagram_code=diagram_code,
            explanation=explanation
        )

    def refine_diagram(self, 
                      process_description: str, 
                      steps: List[str], 
                      current_diagram: str,
                      feedback: str,
                      diagram_history: List[dict]) -> MermaidDiagram:
        """Refina um diagrama existente baseado no feedback do usuário."""
        
        # Template específico para refinamento
        template = """
        Você é um especialista em refinar diagramas Mermaid.
        Analise o histórico de diagramas e o feedback do usuário para criar uma versão melhorada.
        
        Descrição do Processo:
        {description}
        
        Passos do Processo:
        {steps}
        
        Diagrama Atual:
        ```mermaid
        {current_diagram}
        ```
        
        Histórico de Alterações:
        {history}
        
        Feedback do Usuário:
        {feedback}
        
        Por favor, crie uma versão melhorada do diagrama que atenda ao feedback do usuário.
        Mantenha a consistência com as versões anteriores onde apropriado.
        
        Retorne apenas:
        1. O código Mermaid do diagrama
        2. Uma breve explicação das alterações
        
        Formato da resposta:
        ```mermaid
        [código do diagrama aqui]
        ```
        
        Explicação:
        [explicação aqui]
        """
        
        # Prepara o histórico formatado
        history_text = "\n".join(
            f"Versão {i+1}:" + 
            (f"\nFeedback: {v['feedback']}" if v['feedback'] else "") + 
            f"\n{v['diagram_code']}\n"
            for i, v in enumerate(diagram_history[:-1])
        )
        
        # Prepara o prompt
        prompt = ChatPromptTemplate.from_template(template)
        
        # Prepara os dados
        formatted_steps = "\n".join(f"- {step}" for step in steps)
        
        # Cria e executa a chain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = chain.invoke({
                    "description": process_description,
                    "steps": formatted_steps,
            "current_diagram": current_diagram,
            "history": history_text,
            "feedback": feedback
        })
        
        # Processa a resposta da mesma forma que generate_diagram
        response = result['text']
        
        # Extrai o código do diagrama
        diagram_start = response.find("```mermaid")
        if diagram_start == -1:
            raise ValueError("Não foi possível extrair o diagrama da resposta")
            
        diagram_end = response.find("```", diagram_start + 10)
        diagram_code = response[diagram_start + 10:diagram_end].strip()
        
        # Extrai a explicação
        explanation_start = response.find("Explicação:")
        if explanation_start == -1:
            explanation = "Sem explicação disponível"
        else:
            explanation = response[explanation_start + 11:].strip()
        
        return MermaidDiagram(
            diagram_code=diagram_code,
            explanation=explanation
        )

    def formalize_description(self, informal_description: str) -> dict:
        """Formaliza uma descrição informal do processo."""
        if not informal_description:
            raise ValueError("A descrição não pode estar vazia")
        
        template = """
        Você é um especialista em documentação técnica de processos RPA.
        Transforme a descrição informal abaixo em uma descrição técnica profissional.
        
        Descrição Informal:
        {description}
        
        Regras para formalização:
        1. Use linguagem técnica apropriada
        2. Mantenha a clareza e objetividade
        3. Estruture em parágrafos lógicos
        4. Preserve informações importantes
        5. Remova coloquialismos
        
        Retorne a resposta no seguinte formato JSON:
        {{
            "formal_description": "descrição formalizada aqui",
            "changes_made": ["lista de principais alterações feitas"],
            "technical_terms": ["termos técnicos identificados/adicionados"]
        }}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        result = chain.invoke({"description": informal_description})
        
        # Processa e valida a resposta
        try:
            import json
            response = json.loads(result['text'].strip())
            required_keys = ["formal_description", "changes_made", "technical_terms"]
            if not all(key in response for key in required_keys):
                raise ValueError("Resposta da IA incompleta")
            return response
        except Exception as e:
            raise ValueError(f"Erro ao processar resposta da IA: {str(e)}")

    def analyze_process_description(self, description: str) -> dict:
        """Analisa a descrição do processo e sugere melhorias."""
        template = """
        Você é um especialista em análise de processos para automação RPA.
        Analise a seguinte descrição de processo e extraia informações relevantes para automação RPA.
        
        Descrição: {description}
        
        Por favor, identifique e retorne no formato JSON:
        {{
            "steps_as_is": ["passo 1", "passo 2", ...],
            "systems": ["sistema 1", "sistema 2", ...],
            "business_rules": ["regra 1", "regra 2", ...],
            "exceptions": ["exceção 1", "exceção 2", ...],
            "automation_goals": ["objetivo 1", "objetivo 2", ...],
            "kpis": ["kpi 1", "kpi 2", ...]
        }}
        
        Seja específico e detalhado nas sugestões, não se limite apenas a termos genéricos.
        """
        
        try:
            # Gera sugestões iniciais
            chain = LLMChain(llm=self.llm, prompt=ChatPromptTemplate.from_template(template))
            result = chain.invoke({"description": description})
            suggestions = json.loads(result['text'].strip())
            
            # Adiciona inferência de dados do processo
            process_data = self.infer_process_data(description, suggestions.get('steps_as_is', []))
            
            # Estrutura o retorno de forma consistente
            return {
                'steps_as_is': suggestions.get('steps_as_is', []),
                'details': {
                    'steps': suggestions.get('steps_as_is', []),
                    'tools': suggestions.get('systems', []),
                    'data_types': process_data.get('types', []),
                    'data_formats': process_data.get('formats', []),
                    'data_sources': process_data.get('sources', []),
                    'data_volume': process_data.get('volume', 'Médio')
                },
                'business_rules': {
                    'business_rules': suggestions.get('business_rules', []),
                    'exceptions': suggestions.get('exceptions', [])
                },
                'automation_goals': {
                    'automation_goals': suggestions.get('automation_goals', []),
                    'kpis': suggestions.get('kpis', [])
                }
            }
        except Exception as e:
            logger.error(f"Erro ao analisar descrição: {str(e)}")
            # Retorna estrutura vazia mas consistente em caso de erro
            return {
                'steps_as_is': [],
                'details': {
                    'steps': [],
                    'tools': [],
                    'data_types': [],
                    'data_formats': [],
                    'data_sources': [],
                    'data_volume': 'Médio'
                },
                'business_rules': {
                    'business_rules': [],
                    'exceptions': []
                },
                'automation_goals': {
                    'automation_goals': [],
                    'kpis': []
                }
            }

    def validate_and_fix_mermaid(self, mermaid_code: str) -> str:
        """Valida e corrige o código Mermaid usando IA."""
        template = """
        Você é um especialista em sintaxe Mermaid.
        Analise e corrija o código Mermaid abaixo, garantindo que siga as melhores práticas.
        
        Código Original:
        {code}
        
        Regras de Correção:
        1. Mantenha apenas uma declaração flowchart TD
        2. IDs dos nós devem ser únicos e sem caracteres especiais
        3. Conexões devem usar sintaxe correta: A --> B ou A -->|texto| B
        4. Nós de decisão devem usar {{texto}} ao invés de >texto]
        5. Estilos devem estar no formato correto: style id fill:#cor,stroke:#333
        6. Subgraphs devem estar corretamente formatados
        7. Mantenha a identação consistente (4 espaços)
        8. Agrupe os elementos de forma lógica:
           - Primeiro os nós
           - Depois as conexões
           - Por último os estilos
        
        Retorne apenas o código Mermaid corrigido, sem explicações.
        """
        
        try:
            chain = LLMChain(llm=self.llm, prompt=ChatPromptTemplate.from_template(template))
            result = chain.invoke({"code": mermaid_code})
            return result['text'].strip()
        except Exception as e:
            logger.error(f"Erro ao corrigir diagrama: {str(e)}")
            return mermaid_code

    def format_node_text(self, text: str, max_length: int = 25) -> str:
        """Formata o texto do nó para melhor visualização."""
        # Remove espaços extras
        text = ' '.join(text.split())
        
        # Se o texto é menor que o limite, retorna direto
        if len(text) <= max_length:
            return text
        
        # Divide em palavras
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # Verifica se adicionar a palavra excede o limite
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                # Salva linha atual e começa nova linha
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        # Adiciona última linha
        if current_line:
            lines.append(' '.join(current_line))
        
        # Retorna texto com quebras de linha
        return '<br>'.join(lines)

    def generate_process_diagram(self, process_data: dict) -> str:
        """Gera um diagrama Mermaid baseado nos dados do processo."""
        template = """
        Você é um especialista em diagramas UML e Mermaid.
        Crie um diagrama de fluxo que represente o processo RPA descrito abaixo.
        
        Processo: {process_name}
        Descrição: {description}
        
        Etapas do Processo:
        {steps}
        
        Sistemas Utilizados:
        {systems}
        
        Regras de Negócio:
        {rules}
        
        Instruções para o Diagrama:
        1. Use flowchart TD
        2. IDs dos nós devem ser únicos e usar snake_case (ex: validar_dados)
        3. Tipos de nós:
           - Início/Fim: ((texto))
           - Ações: [texto]
           - Decisões: {{texto}}
           - Sistemas: [(texto)]
        4. Conexões:
           - Fluxo simples: A --> B
           - Fluxo com label: A -->|texto| B
        5. Estrutura do código:
           - Primeiro declare todos os nós
           - Depois todas as conexões
           - Por último todos os estilos
        6. Cores e estilos:
           style inicio fill:#f9f9f9,stroke:#333
           style acao fill:#bbdefb,stroke:#333
           style decisao fill:#fff59d,stroke:#333
           style sistema fill:#c8e6c9,stroke:#333
        7. Formatação do texto:
           - Use <br> para quebras de linha
           - Limite cada linha a 25 caracteres
           - Mantenha textos concisos
           - Use 2-3 linhas no máximo por nó
        
        Exemplo de código correto:
        flowchart TD
            inicio((Início))
            validar{{Validar<br>Dados}}
            processar[Processar<br>Informações]
            sistema[(CRM)]
            fim((Fim))

            inicio --> validar
            validar -->|Válido| processar
            validar -->|Inválido| fim
            processar --> sistema
            sistema --> fim

            style inicio fill:#f9f9f9,stroke:#333
            style validar fill:#fff59d,stroke:#333
            style processar fill:#bbdefb,stroke:#333
            style sistema fill:#c8e6c9,stroke:#333
            style fim fill:#f9f9f9,stroke:#333
        
        Retorne apenas o código Mermaid, sem explicações.
        """
        
        try:
            chain = LLMChain(llm=self.llm, prompt=ChatPromptTemplate.from_template(template))
            result = chain.invoke({
                "process_name": process_data.get('process_name', ''),
                "description": process_data.get('process_description', ''),
                "steps": "\n".join(f"- {self.format_node_text(step)}" for step in process_data.get('steps_as_is', [])),
                "systems": "\n".join(f"- {self.format_node_text(system)}" for system in process_data.get('systems', [])),
                "rules": "\n".join(f"- {self.format_node_text(rule)}" for rule in process_data.get('business_rules', []))
            })
            
            # Limpa e valida o código gerado
            mermaid_code = result['text'].strip()
            return self.validate_and_fix_mermaid(mermaid_code)
            
        except Exception as e:
            logger.error(f"Erro ao gerar diagrama: {str(e)}")
            raise ValueError(f"Erro ao gerar diagrama: {str(e)}")

    def infer_process_data(self, description: str, steps: List[str]) -> dict:
        """Infere dados do processo a partir da descrição e passos."""
        template = """Você é um especialista em análise de processos RPA.
Analise a descrição e os passos do processo abaixo e extraia informações sobre os dados manipulados.

Descrição do Processo:
{description}

Passos do Processo:
{steps}

Retorne apenas um objeto JSON com esta estrutura exata, sem texto adicional:
{{
    "types": ["lista de tipos de dados identificados"],
    "formats": ["lista de formatos identificados"],
    "sources": ["lista de fontes identificadas"],
    "volume": "Baixo/Médio/Alto baseado na análise"
}}"""
        
        try:
            # Cria e executa a chain
            chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(template)
            )
            
            # Executa a chain
            result = chain.invoke({
                "description": description,
                "steps": "\n".join(f"- {step}" for step in steps)
            })
            
            # Limpa a resposta e extrai o JSON
            response_text = result['text'].strip()
            
            # Garante que estamos pegando apenas o JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Não foi possível encontrar JSON na resposta")
            
            json_str = response_text[start_idx:end_idx]
            
            # Parse do JSON
            data = json.loads(json_str)
            
            # Validação explícita dos campos
            required_fields = ["types", "formats", "sources", "volume"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                raise ValueError(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao inferir dados do processo: {str(e)}")
            # Retorna valores padrão em caso de erro
            return {
                "types": ["Dados financeiros", "Documentos fiscais"],
                "formats": ["PDF", "Excel"],
                "sources": ["Email", "Sistema"],
                "volume": "Médio"
            }

    def get_mock_description(self) -> str:
        """Retorna uma descrição de processo mock para testes."""
        return """
        Processo de Validação e Processamento de Notas Fiscais Eletrônicas

        O processo inicia quando o departamento financeiro recebe notas fiscais eletrônicas (NFe) por email dos fornecedores. 
        O assistente financeiro acessa a caixa de entrada do Outlook a cada 2 horas para verificar novos emails com NFes anexadas em PDF.

        Para cada nota fiscal recebida, o assistente deve:
        1. Baixar o arquivo PDF do email
        2. Extrair os dados principais usando o sistema OCR interno
        3. Acessar o portal da Receita Federal para validar a autenticidade da NFe
        4. Inserir os dados no sistema SAP, módulo financeiro
        5. Atualizar a planilha de controle no Excel com status e valores
        6. Enviar email de confirmação para o fornecedor
        7. Arquivar o PDF em pasta compartilhada no SharePoint

        Regras importantes:
        - Notas fiscais acima de R$ 50.000 precisam de aprovação do gerente
        - Fornecedor deve estar cadastrado e ativo no SAP
        - Data de emissão não pode ser superior a 30 dias
        - CNPJ do fornecedor deve ser válido
        - Valores e impostos devem estar corretos conforme legislação

        Exceções comuns:
        - Sistema SAP fora do ar
        - PDF ilegível ou corrompido
        - Nota fiscal cancelada ou já processada
        - Divergência nos cálculos de impostos
        - Fornecedor bloqueado ou inativo

        O volume médio é de 200 notas fiscais por dia, com picos de até 500 em fechamento de mês.
        O objetivo é automatizar este processo para reduzir erros de digitação, agilizar o processamento
        e garantir conformidade fiscal. Atualmente, cada nota leva em média 15 minutos para ser processada manualmente.
        """