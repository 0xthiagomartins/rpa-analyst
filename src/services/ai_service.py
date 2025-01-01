"""Serviço de comunicação com IA."""
import json
from typing import Optional, Dict, Any
import openai
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
    
    def __init__(self, api_key: str):
        """
        Inicializa o serviço.
        
        Args:
            api_key: Chave da API OpenAI
        """
        self.cache = InMemoryCache()
        self.logger = Logger()
        openai.api_key = api_key
    
    async def suggest_improvements(
        self, 
        description: str,
        current_data: Optional[Dict] = None
    ) -> AIResponse:
        """
        Sugere melhorias e gera dados estruturados.
        
        Args:
            description: Descrição do processo
            current_data: Dados atuais dos formulários (opcional)
            
        Returns:
            Resposta estruturada da IA
        """
        try:
            # Verifica cache
            cache_key = f"suggestions:{description}"
            cached = self.cache.get(cache_key)
            if cached:
                self.logger.info("Usando resposta em cache")
                return cached
            
            # Gera prompt
            prompt = self._generate_prompt(description, current_data)
            
            # Processa com IA
            self.logger.info("Processando com IA")
            response = await self._process_with_ai(prompt)
            
            # Valida e parseia resposta
            parsed = self._parse_response(response)
            
            # Atualiza cache (24h)
            self.cache.set(cache_key, parsed, ttl=86400)
            
            return parsed
            
        except Exception as e:
            self.logger.error(f"Erro ao processar sugestões: {str(e)}")
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
    
    async def _process_with_ai(self, prompt: str) -> str:
        """Processa prompt com a IA."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Ajuste para acessar o dicionário corretamente
            if isinstance(response, dict):
                return response['choices'][0]['message']['content']
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Erro na chamada à API: {str(e)}")
            raise
    
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
