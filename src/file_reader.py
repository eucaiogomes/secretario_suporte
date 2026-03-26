import os
from pathlib import Path

class FileReader:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        
    def read_all(self) -> list[dict]:
        """
        Lê todos os arquivos .md do vault de forma recursiva.
        Retorna uma lista de dicionários contendo o caminho, nome de arquivo e o texto bruto.
        """
        documents = []
        for md_file in self.vault_path.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                documents.append({
                    "path": str(md_file),
                    "filename": md_file.name,
                    "content": content
                })
            except Exception:
                # Ignoramos silenciosamente erros de leitura, por exemplo, por permissão ou encoding diferente.
                pass
                
        return documents
