import os
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

class ArticleVectorizer:
    def __init__(self, model_name='all-MiniLM-L6-v2', cache_path='data/vector_cache.pkl'):
        self.model = SentenceTransformer(model_name)
        self.cache_path = cache_path
        self.vector_cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_path, 'wb') as f:
            pickle.dump(self.vector_cache, f)

    def vectorize_article(self, article):
        url = article['url']
        if url in self.vector_cache:
            return np.array(self.vector_cache[url])

        text = article['text']
        vector = self.model.encode(text)
        self.vector_cache[url] = vector.tolist()
        self._save_cache()
        return vector

    def batch_vectorize(self, articles):
        return [self.vectorize_article(a) for a in articles]