
# Project Title

A brief description of what this project does and who it's for

# NewsAggregator — AI-Powered News Aggregation & Chatbot

NewsBot is an intelligent web application that automatically scrapes, summarizes, and categories trending news articles. It also features a chatbot powered by Retrieval-Augmented Generation (RAG) that can answer user questions about the latest news corpus.

Built using **Flask**, **OpenAI**, **Transformers**, and **BeautifulSoup**, this project combines natural language processing with practical web development.

---

## 🚀 Features

- 🔎 **News Scraping**: Automatically gathers fresh articles from multiple news sources.
- 🧠 **Summarization**: Uses LLM-powered or rule-based summarization to create concise news summaries.
- 🏷️ **Topic Classification**: Predicts news categories (sports, lifestyle, music, and finance) using machine learning models.
- 🔁 **Duplicate Detection**: Highlights similar articles from different sources.
- 📊 **Frequency Analysis**: Identifies and displays frequently covered topics.
- 🤖 **Chatbot with RAG**: Lets users ask questions about recent news, retrieving relevant articles and generating answers using OpenAI embeddings.
- 🎛️ **Category Filtering**: Users can filter news articles by topic.
- 💾 **Caching & Storage**: Embeddings and URLs are cached to speed up subsequent use.

---

## 🧰 Tech Stack

| Layer             | Tools Used                                      |
|------------------|-------------------------------------------------|
| Backend           | Flask, Python                                   |
| Frontend          | HTML, JS (Fetch API), Jinja2                    |
| NLP & ML          | scikit-learn, NumPy, OpenAI Embeddings          |
| Scraping          | BeautifulSoup, Requests                         |
| Storage & Caching | Pickle, Pandas                                  |
| Deployment        | Heroku-ready                                    |

---

## 📂 Project Structure
``` text
newsbot/
│
├── app.py # Flask app
├── rag_chatbot.py # RAG-based chatbot logic
├── scrape_articles.py # Scraper for news articles
├── summarize.py # Summarizes the article using Transformers
├── classify.py # Classifier (Category prediction using Transformers)
├── embed_openai.py # OpenAI embeddings & caching
├── templates/
│ └── index.html # Webpage template
├── data/
│ ├── highlights.pkl # Article objects
│ ├── openai_embedding_cache.pkl # Article embeddings using openai
│ └── articles_prioritized.pkl # Ordered Article objects
| └── vector_cache.pkl # Article embeddings using Transformers
├── static/
| └── style.css # Web app style
| └── script.js # Question and filter functions on webpage
├── requirements.txt # Python dependencies
└── README.md # This file
```

---

## Project Workflow

```mermaid 
    graph TD
    A[Fetch Articles] --> B[Summarize & Classify];
    B --> C[Keyword Extraction];
    C --> D[Embed with OpenAI];
    D --> E[Store in Pickle Cache];
    E --> F[Display on Web (app.py)];
    E --> G[Answer Questions via RAG Chatbot];
    F --> H[User Filters by Category or Searches];
    G --> I[Flask POST to /ask];
    I --> J[OpenAI returns answer];
```

