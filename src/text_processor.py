import re

class TextProcessor:
    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        Limpa o texto Markdown para deixá-lo focado no conteúdo.
        Remove frontmatter (YAML), códigos bloqueados e excessos de linhas brancas.
        """
        if not text:
            return ""
            
        # 1. Remove YAML frontmatter (tudo entre '---' no topo do arquivo)
        text = re.sub(r'^---[\s\S]*?---\n', '', text)
        
        # 2. Remove blocos de código grandes (que geram ruído pra IA)
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # 3. Remover tags HTML se presentes
        text = re.sub(r'<[^>]+>', '', text)
        
        # 4. Remove múltiplos espaços em branco \n redundantes
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()

    @staticmethod
    def chunk_document(filename: str, path: str, clean_text: str) -> list[dict]:
        """
        V2 Pseudo-Chunking:
        Divide o documento em blocos menores (chunks) baseados em Headers Markdown (# e ##).
        Trata cada bloco como um 'mini-documento'.
        """
        # Adiciona newline no inicio para garantir que o regex pegue o primeiro header se existir
        text_with_nl = "\n" + clean_text
        
        # O regex \n(?=#\s|##\s) faz um split TODA VEZ que encontrar enter seguido por "# " ou "## "
        # O lookahead (?=...) mantém a hashtag no início do chunk
        chunks_raw = re.split(r'\n(?=#\s|##\s)', text_with_nl)
        
        chunks = []
        for i, chunk in enumerate(chunks_raw):
            chunk = chunk.strip()
            
            # Se o bloco for muito pequeno (ex: só um heading ou algo minúsculo), não polui o array
            if len(chunk) < 50:
                continue
                
            # Identificação prompter - pegar a 1a linha para titularização
            first_line = chunk.split('\n')[0][:60]
            section_name = first_line.replace('#', '').strip()
            
            if not section_name:
                section_name = f"Parte {i+1}"
                
            chunks.append({
                "filename": f"{filename} (Seção: {section_name})",
                "path": path,
                "content": chunk,
            })
            
        return chunks
