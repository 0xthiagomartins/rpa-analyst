from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class MermaidDiagram(BaseModel):
    """Modelo para o diagrama Mermaid."""
    diagram_code: str = Field(description="Código do diagrama em sintaxe Mermaid")
    explanation: str = Field(description="Explicação do diagrama gerado")

class AIService:
    """Serviço para geração de diagramas usando IA."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=MermaidDiagram)
    
    def generate_diagram(self, process_description: str, steps: List[str]) -> MermaidDiagram:
        """
        Gera um diagrama Mermaid baseado na descrição do processo.
        
        Args:
            process_description: Descrição textual do processo
            steps: Lista de passos do processo
            
        Returns:
            MermaidDiagram: Objeto contendo o código do diagrama e sua explicação
            
        Raises:
            ValueError: Se os inputs forem inválidos ou houver erro de parsing
            Exception: Se houver erro na geração do diagrama
        """
        # Validação de inputs
        if not process_description or not process_description.strip():
            raise ValueError("A descrição do processo não pode estar vazia")
        
        if not steps or not isinstance(steps, list):
            raise ValueError("Steps deve ser uma lista não vazia")
        
        if not all(isinstance(step, str) and step.strip() for step in steps):
            raise ValueError("Todos os steps devem ser strings não vazias")
        
        try:
            # Prepara os passos formatados
            formatted_steps = "\n".join(f"- {step}" for step in steps)
            
            # Template sem caracteres especiais que podem causar problemas
            template = """
            Você é um especialista em criar diagramas de fluxo usando Mermaid.
            Com base na descrição do processo e seus passos, crie um diagrama de fluxo claro e organizado.
            
            Descrição do Processo:
            {description}
            
            Passos do Processo:
            {steps}
            
            Regras para o diagrama:
            1. Use a sintaxe 'graph TD' para direção top-down
            2. Identifique decisões usando nós com chaves
            3. Use cores e ícones apropriados
            4. Mantenha o diagrama limpo e legível
            5. Adicione descrições claras para cada nó
            6. Use setas com rótulos para indicar condições
            7. Comece cada nó com uma letra maiúscula (A, B, C...)
            
            Exemplo:
            graph TD
                A[Início] --> B[Decisão]
                B --> C[Ação 1]
                B --> D[Ação 2]
            
            {format_instructions}
            """
            
            # Cria o prompt com as variáveis corretas
            prompt = ChatPromptTemplate.from_messages([
                ("system", template)
            ])
            
            chain = LLMChain(
                llm=self.llm,
                prompt=prompt
            )
            
            # Executa a chain com os inputs validados
            try:
                response = chain.invoke({
                    "description": process_description,
                    "steps": formatted_steps,
                    "format_instructions": self.parser.get_format_instructions()
                })
            except Exception as e:
                raise ValueError(f"Erro na chamada da API: {str(e)}")
            
            if not response or 'text' not in response:
                raise ValueError("Resposta inválida da API")
            
            # Parse o resultado
            try:
                result = self.parser.parse(response['text'])
                return result
            except Exception as parse_error:
                raise ValueError(f"Erro ao processar resposta da API: {str(parse_error)}")
            
        except ValueError as ve:
            # Propaga erros de validação
            raise ve
        except Exception as e:
            # Converte outros erros em ValueError para manter consistência
            raise ValueError(f"Erro ao gerar diagrama: {str(e)}")