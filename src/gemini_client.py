import logging
from google import genai
from src.config import AppConfig

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        config = AppConfig()
        if not config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY não configurada!")
            
        self.client = genai.Client(api_key=config.gemini_api_key)
        self.model_name = 'gemini-2.5-flash'
        
    def ask(self, prompt: str) -> str:
        """
        Faz a chamada síncrona para a API do Google Gemini com o prompt gerado.
        Retorna o texto da resposta.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Erro ao contatar a API do Google Gemini: {str(e)}")
            return f"❌ Erro ao contatar a API do Google Gemini: {str(e)}"
