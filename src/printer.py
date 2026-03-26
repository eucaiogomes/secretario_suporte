class Printer:
    @staticmethod
    def print_header(question: str):
        print("="*60)
        print(f"🧠 Faculdade Caio Uninter")
        print(f"❓ Pergunta: {question}")
        print("="*60)
        print("🔍 Analisando seu Vault...\n")
        
    @staticmethod
    def print_answer(answer: str, sources: list[str] = None):
        print("\n" + "="*60)
        print("🤖 RESPOSTA DA IA:")
        print("="*60)
        print(answer)
        print("="*60)
        
        # Mostramos em quais arquivos Markdown o Motor de Busca procurou
        if sources:
            print("\n📚 Fontes consultadas no Obsidian:")
            # Evita arquivos duplicados no display
            for source in list(dict.fromkeys(sources)):
                print(f" - {source}")
            print()
            
    @staticmethod
    def print_error(msg: str):
        print(f"\n❌ ERRO: {msg}")
