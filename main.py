from scraper_australia import NewsScraper
from categorize_news import classify_article
from vectorize_transformers import ArticleVectorizer
from embed_openai import OpenAIArticleEmbedder
from prioritizer_news import prioritize_articles

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os

# Find the stories that are close to each other
def detect_duplicates(articles, vectors, threshold=0.75):
    sim_matrix = cosine_similarity(vectors)
    url_to_similars = {article['url']: [] for article in articles}

    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            if sim_matrix[i][j] > threshold:
                url_i = articles[i]['url']
                url_j = articles[j]['url']
                url_to_similars[url_i].append(url_j)
                url_to_similars[url_j].append(url_i)

    return url_to_similars

# Store these similar articles as attributes
def assign_frequencies(articles, similar_urls_map):
    for article in articles:
        url = article['url']
        article['similar_urls'] = similar_urls_map.get(url, [])
        article['frequency'] = 1 + len(article['similar_urls'])  # self + similar
    return articles

def save_articles(articles, filename='data/articles_prioritized.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(articles, f)

def load_articles(filename='data/articles_prioritized.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return []

def main():
    # Step 1: Scrape articles from the multiple Australian news outlets
    scraper = NewsScraper()
    raw_articles = scraper.scrape_news()
    
    # Step 2: Categorize these articles using a transformer
    '''
    classified_articles = []
    for article in raw_articles:
        predicted = classify_article(article)
        article['category'] = predicted['label']
        article['text'] = predicted['summary']
        classified_articles.append(article)
    '''

    # Load previously retrieved articles
    cached_articles = load_articles('data/articles_prioritized.pkl')
    cached_urls = set(article['url'] for article in cached_articles)

    # Categorize only new articles
    new_articles = []
    
    for article in raw_articles:
        if article['url'] not in cached_urls:
            predicted = classify_article(article)
            article['predicted_category'] = predicted['label']
            article['summarized_text'] = predicted['summary']
            new_articles.append(article)
    
    classified_articles = cached_articles + new_articles
    
    # Step 3: Vectorize using transformers for duplicate detection
    vectorizer = ArticleVectorizer()
    vectors = vectorizer.batch_vectorize(classified_articles)
    
    # Step 4: Get OpenAI Embeddings, used for RAG implementation while question-answering.
    openai_embedder = OpenAIArticleEmbedder()
    openai_embeddings = openai_embedder.batch_embed(classified_articles)
    
    '''
    I have used both types of embeddings, but the system can work with one. 
    I wanted to use them both from a practice point of view
    '''

    # Step 5: Detect duplicates for news articles based on cosine similarity > 0.75
    similar_urls_map = detect_duplicates(classified_articles, vectors)

    # Step 6: Assign frequency (the number of news outlets that reported this news)
    enriched_articles = assign_frequencies(classified_articles, similar_urls_map)

    # Step 7: Assigned a priority score based on (frequency + number of keywords in the article)
    prioritized = prioritize_articles(enriched_articles)

    # Step 8: Save
    save_articles(prioritized)

    # Save highlights for the app
    with open("data/highlights.pkl", "wb") as f:
        pickle.dump(classified_articles, f)

if __name__ == "__main__":
    main()