from flask import Flask, render_template, request, jsonify
import pickle
from rag_chatbot import answer_question
from prioritizer_news import prioritize_articles 
import os

app = Flask(__name__)

# Load highlights from pickle file
def load_highlights():
    with open('data/highlights.pkl', 'rb') as f:
        highlights = pickle.load(f)
    return prioritize_articles(highlights)

prioritized_highlights = prioritize_articles(pickle.load(open('data/highlights.pkl', 'rb')))

# Home page
@app.route('/')
def index():
    categories = set(article['predicted_category'] for article in prioritized_highlights)
    return render_template('index.html', highlights=prioritized_highlights, categories=categories)

# Chatbot Q&A endpoint
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")
    prioritized_highlights = load_highlights()

    try:
        answer = answer_question(question, prioritized_highlights)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})
        

# Filter articles by category
@app.route('/filter', methods=['POST'])
def filter_highlights():
    selected_category = request.form.get('category')
    prioritized_highlights = load_highlights()
    # If the selected category is 'all', show all highlights (same as home page)
    if selected_category == 'all' or selected_category == None:
        filtered_highlights = prioritized_highlights
    else:
        # Filter the articles based on selected category
        filtered_highlights = [article for article in prioritized_highlights if article['predicted_category'] == selected_category]
    
    categories = set(article['predicted_category'] for article in prioritized_highlights)

    return render_template('index.html', highlights=filtered_highlights, categories=categories)

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
