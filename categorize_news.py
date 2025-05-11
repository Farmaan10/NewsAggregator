from transformers import pipeline
import torch

# Categories we want to classify into
LABELS = ["sports", "lifestyle", "music", "finance"]

class ArticleClassifier:
    def __init__(self, use_gpu: bool = True):
        # Determine if a GPU should be used
        device = 0 if use_gpu and torch.cuda.is_available() else -1
        
        # Load the zero-shot classification model (using a dedicated model for classification)
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",  # Switch to a model suited for zero-shot classification
            device=device
        )

        # Load the summarization model
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    def summarize_text(self, text: str) -> str:
        """Summarize long article text."""
        max_length = 1024  # BART has a max input size limit
        if len(text) > max_length:
            text = text[:max_length]  # Truncate long articles (can also split the text into chunks if needed)
        
        # Summarize the article text
        try:
            summary = self.summarizer(text, max_length=120, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error during summarization: {e}")
            return text  # Return original text if summarization fails

    def classify(self, article) -> str:
        """Classify the article into categories."""
        text = article.get('title', '') + "\n" + article.get('text', '')
        
        # Summarize the article text before classification
        summarized_text = self.summarize_text(text)

        # Classify the summarized text
        result = self.classifier(text, LABELS)

        # Return the top predicted label
        return {
            "label": result['labels'][0],
            "summary": summarized_text
    }

# Singleton instance for use in main
_classifier_instance = ArticleClassifier()

def classify_article(article):
    """Wrapper to access the singleton classifier instance."""
    return _classifier_instance.classify(article)


'''
from transformers import pipeline
import torch

# Categories we want to classify into
LABELS = ["sports", "lifestyle", "music", "finance"]

class ArticleClassifier:
    def __init__(self, use_gpu: bool = True):
        device = 0 if use_gpu and torch.cuda.is_available() else -1
        self.classifier = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-3",
            device=device
        )

    def classify(self, article) -> str:
        text = article.get('title', '') + "\n" + article.get('text', '')
        result = self.classifier(text, LABELS)
        return result['labels'][0]  # Return the top predicted label

# Singleton instance for use in main
_classifier_instance = ArticleClassifier()

def classify_article(article):
    return _classifier_instance.classify(article)
'''