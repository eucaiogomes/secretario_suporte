from src.models import Document

class ContextBuilder:
    def __init__(self, max_chars: int = 40000):
        # V2: Com TF-IDF as fontes são mais ricas. Aumentamos a tolância para cerca de 10.000 tokens
        self.max_chars = max_chars
        
    def build_context(self, relevant_docs: list[Document]) -> str:
        """
        V2: Concatena de forma estruturada para o LLM não se perder
        """
        context_parts = []
        current_length = 0
        
        for doc in relevant_docs:
            # Layout mais claro exigido na V2
            header = f"\n[Fonte: {doc.filename}]\n"
            content = doc.content
            
            # Espaço que ainda temos sobrando
            available_space = self.max_chars - current_length - len(header)
            
            if available_space <= 0:
                break
                
            # Truncar o documento se ele for gigantesco e estourar o restante
            if len(content) > available_space:
                content = content[:available_space] + "\n...[Conteúdo truncado devido ao limite de contexto]"
                
            part = header + content
            context_parts.append(part)
            current_length += len(part)
            
            if current_length >= self.max_chars:
                break
                
        if not context_parts:
            return "A busca não encontrou nenhuma informação relevante sobre sua pergunta no Vault."
            
        return "\n".join(context_parts)
