import os
import pickle
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class OpenAIArticleEmbedder:
    def __init__(self, model_name="text-embedding-3-small", cache_path='data/openai_embedding_cache.pkl'):
        self.model_name = model_name
        self.cache_path = cache_path
        self.embedding_cache = self._load_cache()
    
    # Get previously embedded articles using openai - saves money by not reusing the openai capabilities
    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_path, 'wb') as f:
            pickle.dump(self.embedding_cache, f)

    # Function to embed the article
    def embed_article(self, article):
        url = article['url']
        if url in self.embedding_cache:
            return np.array(self.embedding_cache[url])

        response = client.embeddings.create(
            input=article['text'],
            model=self.model_name
            )
        
        embedding = response.data[0].embedding
        self.embedding_cache[url] = embedding 
        article['openai_embedding'] = embedding # Adds it as an article object attribute
        self._save_cache()
        return np.array(embedding)

    # Find openai embeddings for list of articles
    def batch_embed(self, articles):
        return [self.embed_article(a) for a in articles]