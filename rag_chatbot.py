# rag_chatbot.py
from openai import OpenAI
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
'''
# Convert question to embedding using OpenAI (or another embedding model)
def get_question_embedding(question):
    response = openai.Embedding.create(
        input=question,
        model="text-embedding-3-small"
    )
    return np.array(response['data'][0]['embedding'])
'''

def get_question_embedding(question):
    response = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)

# Retrieve top-k most relevant articles using cosine similarity
def retrieve_relevant_articles(question_embedding, articles, top_k=3):
    article_embeddings = np.array([np.array(article['openai_embedding']) for article in articles])
    similarities = cosine_similarity([question_embedding], article_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [articles[i] for i in top_indices]

# Use GPT to generate an answer given the retrieved context
def generate_answer(question, retrieved_articles):
    context = context = "\n".join(f"{a['title']} ({a['date']}): {a['text']}" for a in retrieved_articles)
    
    prompt = f"""You are a well-informed and concise assistant specialized in answering question after analyzing current news.
    
    Use the article excerpts below to answer the user's question. Focus only on the information provided in the context. Be accurate, avoid speculation, and clearly cite relevant facts or sources from the excerpts when needed.
    
    Context: {context}
    
    User Question: {question}
    
    Answer:"""

    '''
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful news assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response['choices'][0]['message']['content'].strip()

    '''
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful news assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# Master function to answer a question
def answer_question(question, articles):
    question_embedding = get_question_embedding(question)
    retrieved_articles = retrieve_relevant_articles(question_embedding, articles)
    return generate_answer(question, retrieved_articles)