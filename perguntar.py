import argparse
import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao sys.path para garantir que o 'src' seja encontrado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.file_reader import FileReader
from src.text_processor import TextProcessor
from src.search_engine import SearchEngine
from src.context_builder import ContextBuilder
from src.prompt_builder import PromptBuilder
from src.llm_router import LLMRouter
from src.printer import Printer
from src.config import AppConfig

def main():
    parser = argparse.ArgumentParser(description="Obsidian AI Knowledge CLI")
    parser.add_argument("question", help="Sua pergunta para a base de conhecimento")
    parser.add_argument("--path", help="Caminho para o Obsidian Vault (opcional)", default=None)
    
    args = parser.parse_args()
    
    try:
        config = AppConfig()
    except Exception as e:
        Printer.print_error(f"Erro de configuração inicial: {e}")
        sys.exit(1)

    vault_path = args.path or config.vault_path
    
    if not vault_path or not os.path.exists(vault_path):
        Printer.print_error(f"O caminho do Vault não foi configurado ou é inválido: '{vault_path}'")
        sys.exit(1)
        
    Printer.print_header(args.question)
    
    try:
        config.validate_keys()

        # 1. Leitura Inicial dos Arquivos
        reader = FileReader(vault_path)
        raw_documents = reader.read_all()
        
        if not raw_documents:
            Printer.print_error("Nenhum arquivo .md foi encontrado no Vault.")
            sys.exit(1)
            
        # 2. Processador de Texto (Limpeza e Pseudo-Chunking)
        clean_docs = []
        for doc in raw_documents:
            clean_text = TextProcessor.clean_markdown(doc.content)
            if clean_text:
                # Quebra em mini-documentos baseados em headings (# / ##)
                chunks = TextProcessor.chunk_document(doc.filename, doc.path, clean_text)
                clean_docs.extend(chunks)
                
        # 3. Motor de Busca (TF-IDF com Top 15 V2)
        top_docs = SearchEngine.search(args.question, clean_docs, top_k=15)
        
        # 4. Construção do Contexto unificado delimitando em segurança os tokens
        context_builder = ContextBuilder(max_chars=20000)
        context = context_builder.build_context(top_docs)
        
        sources = [doc.filename for doc in top_docs]
        
        # 5. Montagem do Prompt Final
        prompt = PromptBuilder.build(args.question, context)
        
        # 6. Comunicação com a API (LLM Router com Fallbacks)
        router = LLMRouter()
        answer = router.generate_response(prompt, context)
        
        # 7. Renderização na Tela
        Printer.print_answer(answer, sources)
        
    except Exception as e:
        Printer.print_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
