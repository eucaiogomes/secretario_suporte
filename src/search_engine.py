import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.gemini_client import GeminiClient
from src.models import Document

logger = logging.getLogger(__name__)

class SearchEngine:
    @staticmethod
    def expand_query(query: str) -> str:
        """
        V2 Query Expansion: Pede ao Gemini sinônimos para escalar o TF-IDF.
        """
        try:
            client = GeminiClient()
            prompt = f"Me dê apenas 5 palavras soltas que sejam sinônimas ou relacionadas ao assunto '{query}'. Sem frases, sem explicações."
            expanded = client.ask(prompt)
            if "Erro" in expanded or len(expanded) > 200:
                return query
            return f"{query} {expanded.strip()}"
        except:
            return query

    @staticmethod
    def search(query: str, documents: list[Document], top_k: int = 15) -> list[Document]:
        """
        V2 Ranking via scikit-learn TfidfVectorizer com Query Expansion e Heading Boost.
        """
        if not documents:
            return []
            
        expanded_query = SearchEngine.expand_query(query)
        logger.info(f"🔄 Expansion V2: Buscando por '{expanded_query.replace(chr(10), ' ')}'")
        
        corpus = [doc.content for doc in documents]
        
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vec = vectorizer.transform([expanded_query])
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            scored_docs = []
            for idx, doc in enumerate(documents):
                score = float(similarities[idx])
                
                # Boost (Headings/Títulos) V2
                words = query.lower().split()
                if any(w in doc.filename.lower() for w in words if len(w) > 3):
                    score *= 1.5
                    
                if score > 0.02:
                    import copy
                    doc_with_score = copy.copy(doc)
                    doc_with_score.score = score
                    scored_docs.append(doc_with_score)
                    
            scored_docs.sort(key=lambda x: x.score, reverse=True)
            
            # Deduplicação: máx de 3 blocos do mesmo arquivo original
            final_docs = []
            seen = {}
            for doc in scored_docs:
                base_name = doc.filename.split(" (Seção")[0]
                if seen.get(base_name, 0) < 3:
                    final_docs.append(doc)
                    seen[base_name] = seen.get(base_name, 0) + 1
                if len(final_docs) >= top_k:
                    break
            return final_docs
        except Exception as e:
            logger.error(f"Erro TF-IDF: {e}")
            return []
