"""Serviço de comunicação com IA."""
import json
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.utils.cache import InMemoryCache
from src.utils.logger import Logger
from .ai_types import AIResponse, FormData

class AIService:
    """Serviço de comunicação com IA."""
    
    SYSTEM_PROMPT = """
    Você é um assistente especializado em análise e documentação de processos. 
    Seu objetivo é analisar descrições de processos e:
    1. Formalizar a descrição
    2. Identificar elementos estruturais
    3. Sugerir melhorias
    4. Gerar dados estruturados para documentação

    Siga estritamente o formato de resposta especificado.
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        Inicializa o serviço.
        
        Args:
            model_name: Nome do modelo a ser usado
        """
        self.logger = Logger()
        self.cache = InMemoryCache()
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7
        )

    async def analyze_process(
        self,
        description: str,
        current_data: Optional[Dict] = None
    ) -> AIResponse:
        """
        Analisa descrição do processo e gera sugestões.
        
        Args:
            description: Descrição do processo
            current_data: Dados atuais dos formulários
            
        Returns:
            AIResponse com sugestões e dados
        """
        try:
            # Tenta obter do cache primeiro
            cache_key = f"analysis_{hash(description)}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached
                
            # Gera prompt
            prompt = self._generate_prompt(description, current_data)
            
            # Prepara mensagens
            messages = [
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]
            
            # Faz requisição via LangChain
            response = await self.llm.agenerate([messages])
            result = self._parse_response(response.generations[0][0].text)
            
            # Salva no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar processo: {str(e)}")
            raise
    
    def _generate_prompt(
        self, 
        description: str,
        current_data: Optional[Dict] = None
    ) -> str:
        """Gera prompt para a IA."""
        prompt = f"""
        Analise a seguinte descrição de processo:

        {description}

        Formate sua resposta como JSON com:
        1. Descrição formal e estruturada
        2. Dados para cada formulário do processo
        3. Sugestões de melhoria
        4. Validações e avisos
        """
        
        if current_data:
            prompt += f"\n\nDados atuais dos formulários:\n{json.dumps(current_data, indent=2)}"
            
        return prompt
    
    def _parse_response(self, response: str) -> AIResponse:
        """
        Parseia e valida resposta da IA.
        
        Args:
            response: Resposta em texto da IA
            
        Returns:
            Resposta estruturada e validada
        """
        try:
            # Parseia JSON
            data = json.loads(response)
            
            # Valida estrutura básica
            required = {'description', 'forms_data', 'suggestions', 'validation'}
            if not all(k in data for k in required):
                raise ValueError("Resposta incompleta da IA")
            
            # Valida dados dos formulários
            for form_id, form_data in data['forms_data'].items():
                if not isinstance(form_data, dict):
                    raise ValueError(f"Dados inválidos para formulário {form_id}")
            
            return AIResponse(
                description=data['description'],
                forms_data=data['forms_data'],
                suggestions=data['suggestions'],
                validation=data['validation']
            )
            
        except json.JSONDecodeError:
            self.logger.error("Falha ao decodificar JSON da resposta")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao parsear resposta: {str(e)}")
            raise
