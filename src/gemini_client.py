import os
from google import genai
from dotenv import load_dotenv

# Carrega a GEMINI_API_KEY do arquivo .env
load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não foi encontrada configurada no .env!")
            
        # O Google atualizou a biblioteca para google-genai (genai.Client) e também as versões dos modelos
        self.client = genai.Client(api_key=api_key)
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
            return f"❌ Erro ao contatar a API do Google Gemini: {str(e)}"
