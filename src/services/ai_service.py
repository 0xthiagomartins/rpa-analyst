from dataclasses import dataclass
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

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