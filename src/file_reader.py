import logging
from pathlib import Path
from src.models import Document

logger = logging.getLogger(__name__)

class FileReader:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        
    def read_all(self) -> list[Document]:
        """
        Lê todos os arquivos .md do vault de forma recursiva.
        Retorna uma lista de objetos Document.
        """
        documents = []
        for md_file in self.vault_path.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                documents.append(Document(
                    path=str(md_file),
                    filename=md_file.name,
                    content=content
                ))
            except (PermissionError, UnicodeDecodeError) as e:
                logger.warning(f"Ignorando arquivo silenciosamente {md_file.name}: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado ao ler {md_file.name}: {e}")
                
        return documents
