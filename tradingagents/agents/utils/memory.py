import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests
load_dotenv()
class FinancialSituationMemory:
    def __init__(self, name="testing"):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=google_api_key)
        self.embedding_model = "models/embedding-001"
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.create_collection(name=name)
        self.embedding_cache = {}
        
        # Configure API endpoints for embedding and sentiment models running in Colab
        self.embedding_api_url = os.getenv("EMBEDDING_API_URL", "http://localhost:8000/embed")
        self.sentiment_api_url = os.getenv("SENTIMENT_API_URL", "http://localhost:8000/sentiment")

    def preprocess_prompt(self, text):
        # Remove excessive whitespace and boilerplate
        text = text.strip()
        # Skip error messages and empty prompts
        if not text or text.lower().startswith("i am sorry"):
            return None
        return text

    def get_embedding(self, text):
        """Get Gemini embedding for a text, with prompt optimization and caching."""
        processed = self.preprocess_prompt(text)
        if processed is None:
            return None
        # Optimization: Check cache first
        if processed in self.embedding_cache:
            return self.embedding_cache[processed]
        try:
            embedding_result = genai.embed_content(
                model=self.embedding_model,
                content=processed,
                task_type="retrieval_document"
            )
            embedding = embedding_result["embedding"]
            self.embedding_cache[processed] = embedding
            return embedding
        except Exception as e:
            print(f"[Prompt Optimization] Gemini embedding error: {e}")
            return None

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using Gemini embeddings"""
        query_embedding = self.get_embedding(current_situation)
        if query_embedding is None:
            print("[Memory] No valid embedding obtained; returning empty memories.")
            return []
        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results

    # New function to call the embedding API
    def call_embedding_api(self, text):
        """Call the external API hosted in Colab to get embeddings."""
        payload = {"text": text}
        try:
            response = requests.post(self.embedding_api_url, json=payload)
            if response.status_code == 200:
                return response.json().get("embedding")
            else:
                print(f"Embedding API error: {response.status_code} {response.text}")
                return None
        except Exception as e:
            print(f"Exception calling embedding API: {e}")
            return None

    # New function to call the sentiment API
    def call_sentiment_api(self, text):
        """Call the external API hosted in Colab to get sentiment analysis."""
        payload = {"text": text}
        try:
            response = requests.post(self.sentiment_api_url, json=payload)
            if response.status_code == 200:
                return response.json().get("sentiment")
            else:
                print(f"Sentiment API error: {response.status_code} {response.text}")
                return None
        except Exception as e:
            print(f"Exception calling sentiment API: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory()

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
