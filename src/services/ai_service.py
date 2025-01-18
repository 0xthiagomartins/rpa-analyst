"""Serviço de IA para sugestões e melhorias."""
from typing import Dict, Any, Optional
import json
import openai
from utils.logger import Logger
from utils.cache import InMemoryCache
from services.validator_service import ValidatorService, ValidationResult

class AIService:
    """Serviço para interação com IA."""
    
    def __init__(self, validator: Optional[ValidatorService] = None):
        """
        Inicializa o serviço.
        
        Args:
            validator: Validador de sugestões opcional
        """
        self.logger = Logger()
        self.cache = InMemoryCache()
        self.validator = validator or ValidatorService()

    async def suggest_improvements(
        self, 
        description: str,
        current_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sugere melhorias para o processo.
        
        Args:
            description: Descrição do processo
            current_data: Dados atuais do processo (opcional)
            
        Returns:
            Dict com sugestões de melhoria
        """
        # Tenta recuperar do cache
        cache_key = f"suggestions:{description}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Prepara o prompt
            messages = [{
                "role": "user",
                "content": self._build_prompt(description, current_data)
            }]

            # Chama a API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )

            # Processa a resposta
            if not response or 'choices' not in response:
                raise ValueError("Resposta inválida da API")
                
            content = response['choices'][0]['message']['content']
            result = self._parse_response(content)

            # Valida as sugestões
            validation = self.validator.validate_suggestions(result)
            if not validation.is_valid:
                raise ValueError(f"Sugestões inválidas: {validation.errors}")

            # Salva no cache
            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            self.logger.error(f"Erro ao gerar sugestões: {str(e)}")
            raise

    def _build_prompt(
        self, 
        description: str,
        current_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Constrói o prompt para a IA."""
        prompt = f"Analise o seguinte processo e sugira melhorias:\n\n{description}\n"
        
        if current_data:
            prompt += f"\nDados atuais:\n{json.dumps(current_data, indent=2)}"
            
        return prompt

    def _parse_response(self, content: str) -> Dict[str, Any]:
        """
        Processa a resposta da IA.
        
        Args:
            content: Conteúdo da resposta
            
        Returns:
            Dict com dados processados
            
        Raises:
            ValueError: Se a resposta for inválida
        """
        try:
            if isinstance(content, str):
                data = json.loads(content)
            else:
                data = content

            # Valida estrutura básica
            required = {'description', 'forms_data', 'suggestions', 'validation'}
            if not all(field in data for field in required):
                raise ValueError("Dados inválidos")

            return data
            
        except json.JSONDecodeError:
            raise ValueError("Resposta inválida da IA")
        except Exception as e:
            raise ValueError(f"Erro ao processar resposta: {str(e)}")
