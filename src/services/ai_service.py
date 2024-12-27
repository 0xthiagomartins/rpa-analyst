from dataclasses import dataclass
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import json
import logging
from src.utils.diagram_validator import DiagramValidator

logger = logging.getLogger(__name__)

@dataclass
class MermaidDiagram:
    """Classe para armazenar o diagrama e sua explicação."""
    diagram_code: str
    explanation: str

class AIService:
    """Serviço para geração de conteúdo usando IA."""
    
    def __init__(self, llm=None):
        # Se não for fornecido um LLM, cria um novo
        self.llm = llm if llm is not None else ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        self.diagram_validator = DiagramValidator()
    
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
        """Analisa a descrição do processo e retorna sugestões estruturadas."""
        try:
            # Template atualizado e corrigido
            template = """Você é um especialista em análise de processos RPA.
Analise a descrição do processo abaixo e extraia informações estruturadas.

Descrição do Processo:
{description}

Ao analisar o processo, considere as seguintes regras de validação do diagrama:
1. Deve haver exatamente um ponto de início
2. Deve haver pelo menos um ponto de fim
3. Todos os nós devem estar conectados
4. Não deve haver ciclos que causem loops infinitos
5. Todas as conexões devem ser entre nós existentes

Retorne um objeto JSON com a seguinte estrutura, sem texto adicional:
{{
    "steps_as_is": ["lista ordenada de etapas"],
    "details": {{
        "steps": ["lista detalhada de etapas"],
        "tools": ["sistemas e ferramentas identificados"],
        "data_types": ["tipos de dados manipulados"],
        "data_formats": ["formatos de dados"],
        "data_sources": ["fontes de dados"],
        "data_volume": "Baixo/Médio/Alto"
    }},
    "business_rules": {{
        "business_rules": ["regras identificadas"],
        "exceptions": ["exceções identificadas"]
    }},
    "automation_goals": {{
        "automation_goals": ["objetivos da automação"],
        "kpis": ["KPIs sugeridos"]
    }},
    "diagram_validation": {{
        "start_node": "identificador do nó inicial",
        "end_nodes": ["identificadores dos nós finais"],
        "connections": [{{"source": "id_origem", "target": "id_destino"}}]
    }}
}}"""
            # Executa a análise
            chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(template)
            )
            
            result = chain.invoke({"description": description})
            
            # Processa e valida o resultado
            data = self._process_ai_response(result['text'])
            
            # Valida o diagrama sugerido
            if 'diagram_validation' in data:
                nodes = self._convert_steps_to_nodes(data['steps_as_is'])
                edges = data['diagram_validation'].get('connections', [])
                
                is_valid, errors = self.diagram_validator.validate_diagram(nodes, edges)
                if not is_valid:
                    logger.warning(f"Diagrama sugerido tem problemas: {errors}")
                    # Tenta corrigir o diagrama
                    data = self._fix_diagram_issues(data, errors)
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao analisar descrição: {str(e)}")
            return {}

    def _convert_steps_to_nodes(self, steps: List[str]) -> List[Dict]:
        """Converte lista de etapas em nós do diagrama."""
        return [
            {
                'id': f"step_{i}",
                'name': step,
                'type': 'action' if i not in [0, len(steps)-1] 
                        else ('start' if i == 0 else 'end')
            }
            for i, step in enumerate(steps)
        ]

    def _fix_diagram_issues(self, data: Dict, errors: List[str]) -> Dict:
        """Tenta corrigir problemas identificados no diagrama."""
        steps = data['steps_as_is']
        
        # Garante nó inicial
        if "nó de início" in " ".join(errors):
            if steps:
                steps.insert(0, "Início do processo")
        
        # Garante nó final
        if "nó de fim" in " ".join(errors):
            steps.append("Fim do processo")
        
        # Atualiza conexões
        connections = []
        for i in range(len(steps)-1):
            connections.append({
                'source': f"step_{i}",
                'target': f"step_{i+1}"
            })
        
        # Atualiza o diagrama validado
        data['diagram_validation'] = {
            'start_node': "step_0",
            'end_nodes': [f"step_{len(steps)-1}"],
            'connections': connections
        }
        
        return data

    def _process_ai_response(self, response: str) -> dict:
        """Processa e valida a resposta da IA."""
        try:
            # Extrai apenas o JSON da resposta
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("JSON não encontrado na resposta")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Validação básica dos campos
            required_fields = ["steps_as_is", "details", "business_rules", "automation_goals"]
            if not all(field in data for field in required_fields):
                raise ValueError("Campos obrigatórios ausentes na resposta")
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao processar resposta da IA: {str(e)}")
            raise

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
            return {
                "types": ["Dados financeiros", "Documentos fiscais"],
                "formats": ["PDF", "Excel"],
                "sources": ["Email", "Sistema"],
                "volume": "Médio"
            }
