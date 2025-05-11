# NewsAggregator — AI-Powered News Aggregation & Chatbot

NewsAggregator is an intelligent web application that automatically extracts news from Australian news outlets across categories such as sports, lifestyle, music, and finance.

It features a built-in chatbot powered by Retrieval-Augmented Generation (RAG), allowing users to ask questions about the most recent news corpus. The chatbot generates answers using OpenAI’s GPT-4.1 model, providing concise and relevant responses based on recent articles.
## Features

- **News Scraping**: Automatically gathers fresh articles from multiple news sources.
- **Summarization**: Uses Transformer powered summarization to create concise news summaries.
- **Topic Classification**: Predicts news categories (sports, lifestyle, music, and finance) using Transformer models.
- **Duplicate Detection**: Highlights similar articles from different sources.
- **Frequency Analysis**: Identifies and displays the frequency of sources that covered the topic.
- **Chatbot with RAG**: Lets users ask questions about recent news, retrieving relevant articles and generating answers using OpenAI embeddings.
- **Category Filtering**: Users can filter news articles by topic.
- **Caching & Storage**: Embeddings and URLs are cached to speed up subsequent use.
## Installation

### Local Setup

#### 1. Clone the Repo

```bash
git clone https://github.com/Farmaan10/NewsAggregator.git
```


#### 2. Set Up Virtual Environment

```bash
cd NewsAggregator
python -m venv newsbot-env

# For Windows:
.\newsbot-env\Scripts\activate

# For macOS/Linux:
source newsbot-env/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Add Environment Variable
Create a .env file in the root directory with:
```
OPENAI_API_KEY=Your_API_Key
```

### Data update
Run this as frequently as you want to fetch and preprocess the latest news, it ignores the ones already in the data:

```bash
python main.py
```
This updates the files in the data/ folder used by the app and chatbot.

### Run the Application
Run this to activate the web app on local environment:

```bash
python app.py
```

Navigate to:
```
http://127.0.0.1:5000/
```    
## Deployment

### Deploying to Render
This project is deployed for free using [Render](https://render.com/), which hosts the Flask web application. Below are the steps and supporting tools used for seamless deployment and automation

#### 1. Hosting on Render
- The Flask app.py is deployed as a Web Service on Render.

- The repository is directly connected to GitHub so that any changes pushed to the main branch are automatically deployed.

- Important: Set the OPENAI_API_KEY in your Render Environment Variables to allow the app to access OpenAI services securely.

#### 2. Preventing Sleep (Free Plan Limitation)
- Since free Render plans can sleep after periods of inactivity, [UptimeRobot](https://uptimerobot.com/) is used to ping the app every 5 minutes, keeping it awake.

- Create a free account on UptimeRobot.

- Set up a "HTTP(s)" monitor that pings your deployed URL every 5 minutes.

#### 3. Scheduled Updates with GitHub Actions
To update the data frequently (via main.py), GitHub Actions is used instead of a paid cron job through Render.

- The workflow is defined in .github/workflows/data_pipeline.yaml.

- It runs main.py on a daily schedule (At Adelaide's midnight).

- Make sure to add your OPENAI_API_KEY to the GitHub repository secrets under Settings > Secrets and variables > Actions.
## Working Snippet

![Recent News](https://github.com/Farmaan10/NewsAggregator/blob/main/ChatBot%20RAG%20working.PNG)