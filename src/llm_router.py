import logging
import time
import concurrent.futures
from google import genai
from groq import Groq
from src.config import AppConfig

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):
        config = AppConfig()
        config.validate_keys()
            
        self.gemini_client = genai.Client(api_key=config.gemini_api_key)
        self.groq_client = Groq(api_key=config.groq_api_key)
        
        self.gemini_model = 'gemini-2.5-flash'
        self.groq_model = 'llama3-8b-8192' 
        
        self.cache = {}
        
    def _retry_with_backoff(self, func, max_retries=3):
        """
        Executa a função providenciada com limite de falhas e backoff exponencial
        caso receba o erro 503, 429 ou 'UNAVAILABLE'.
        """
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                error_msg = str(e).lower()
                if "503" in error_msg or "unavailable" in error_msg or "429" in error_msg:
                    wait_time = 2 ** attempt
                    if attempt < max_retries - 1:
                        logger.warning(f"🔄 [Retry] Chamada falhou. Aguardando {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e
                else:
                    raise e
        raise Exception("Falha após múltiplas tentativas.")

    def _call_gemini(self, prompt: str) -> str:
        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt
        )
        return response.text

    def _call_groq(self, prompt: str) -> str:
        completion = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, 
        )
        return completion.choices[0].message.content

    def _local_fallback(self, context: str) -> str:
        safe_context = context[:2500] if context else "Nenhum contexto encontrado."
        return f"""⚠️ **Aviso de Fallback Local Ativado** ⚠️
Não foi possível gerar uma resposta sintética com Inteligência Artificial neste momento (APIs inoperantes ou tempo limite excedido).

**Exibindo os trechos de contexto brutos encontrados na sua base de notas:**

{safe_context}...
"""

    def generate_response(self, prompt: str, context: str, timeout_sec: int = 20) -> str:
        """
        Tenta buscar no cache ou invocar as LLMs (com fallback) com timeout de segurança.
        """
        cache_key = hash(prompt)
        
        if cache_key in self.cache:
            logger.info("🚀 [Cache] Resposta recuperada instantaneamente da memória!")
            return self.cache[cache_key]

        def _execute_pipeline():
            try:
                return self._retry_with_backoff(lambda: self._call_gemini(prompt))
            except Exception as gemini_err:
                logger.warning(f"⚠️ [Fallback] Falha no Gemini: {gemini_err}. Pivotando para Groq.")
                try:
                    return self._retry_with_backoff(lambda: self._call_groq(prompt))
                except Exception as groq_err:
                    logger.error(f"❌ [Fallback] Groq também falhou: {groq_err}. Recorrendo ao Fallback Local.")
                    return self._local_fallback(context)

        answer = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_execute_pipeline)
            try:
                answer = future.result(timeout=timeout_sec)
            except concurrent.futures.TimeoutError:
                logger.error(f"⏳ [Timeout] O limite estourou ({timeout_sec}s). Retornando fallback local.")
                answer = self._local_fallback(context)

        if answer and "Aviso de Fallback Local Ativado" not in answer:
            self.cache[cache_key] = answer

        return answer
