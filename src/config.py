import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Configurar logging base
        self._setup_logging()
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Carregar settings.json
        self.settings = self._load_settings()
        self.vault_path = self.settings.get("vault_path")

    def _setup_logging(self):
        # Apenas mensagens essenciais no terminal (logs de INFO serão exibidos como avisos amigáveis pelo Printer ou logger dependendo de como preferimos)
        # Vamos manter logger para diagnosticos e erro s, usando formato limpo.
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        # Ajustar nível do logger raiz se desejar menos verbosidade 
        # (ex: WARNING para ignorar infos soltas)
        # Para CLIs, às vezes formatar sem data é melhor, mas vamos deixar simples.
        # Desliga logs de blibiotecas verbosas
        logging.getLogger("httpx").setLevel(logging.WARNING)

    def _load_settings(self) -> dict:
        settings_path = Path(__file__).parent.parent / "config" / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.getLogger(__name__).warning(f"Não foi possível carregar settings.json: {e}")
        return {}
        
    def validate_keys(self):
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY não foi encontrada configurada no .env!")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY não foi encontrada configurada no .env!")
