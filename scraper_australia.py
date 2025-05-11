import requests
from bs4 import BeautifulSoup
import re
from langchain_community.document_loaders import NewsURLLoader
import pandas as pd
import os
import pickle

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.existing_urls = self.load_existing_urls() 
    
    # load previously scraped urls
    def load_existing_urls(self, file_path='data/articles_prioritized.pkl'):
        if os.path.exists(file_path):
            with open('data/articles_prioritized.pkl', 'rb') as f:
                articles = pickle.load(f)
                return {article['url'] for article in articles if 'url' in article}
        return set()

    def scrape_news(self): # Main scraping function
        articles = []

        # Get article URLs from category pages of news outlets
        for category, urls in self._get_category_urls().items():
            for url in urls:
                article_urls = self._get_article_urls(url, category)

                #addition when adding pickle file -> check existing urls and only consider new ones
                existing_links = self.existing_urls  # load URLs from previous pickle
                article_urls = [url for url in article_urls if url not in existing_links]

                articles.extend(self._load_articles(article_urls, category)) #addition when adding pickle file
        
        print(f"New articles added: {len(articles)}")

        return articles
    
    def _get_category_urls(self):
        # Hardcoded category URLs
        return {
            "sports": ["https://www.7news.com.au/sport", "https://www.theage.com.au/sport"],
            "lifestyle": ["https://www.7news.com.au/lifestyle", "https://www.theage.com.au/lifestyle"],
            "music": ["https://www.7news.com.au/entertainment/music", "https://www.theage.com.au/culture/music"],
            "finance": ["https://www.7news.com.au/business/finance", "https://www.theage.com.au/business/banking-and-finance"]
        }
    
    def _get_article_urls(self, category_url, category):
        # Extract article links from a category page
        try:
            response = requests.get(category_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if self._is_valid_article_link(href, category):
                    full_url = self._make_full_url(href, category_url)
                    links.append(full_url)
            
            return list(set(links))
                
        except Exception as e:
            print(f"Error scraping {category_url}: {str(e)}")
            return []
    
    def _is_valid_article_link(self, href, category):
        
        # Changed approach that automatically removes most of these
        bad_links = [
            "twitter.com", "facebook.com", "instagram.com", "youtube.com", "/x.com",
            "tiktok.com", "coupons.7news", "support.7news", "mailto", "7plus.com.au",
            "about-us", "my_account", "terms-and-conditions", "advertisers.com.au"
        ]
        
        # Exclude non-article links
        if href.startswith("http"):
            return False 

        # Exclude links that start with "/video"
        if href.startswith("/video"):
            return False

        return (
            len(href)>25 and
            not any(p in href for p in bad_links)
        )
    
    def _make_full_url(self, href, base_url):
        # Findinf the domain from URLs

        if href.startswith('http'):
            return href
        domain = base_url.split('/')[2]
        return f"https://{domain}{href if href.startswith('/') else '/' + href}"


    # Store modified _load_articles
    def _load_articles(self, urls, category):
        new_articles = []
        loader = NewsURLLoader(urls=urls)
        docs = loader.load()

        for doc in docs:
            article_url = doc.metadata.get('link')
            if article_url in self.existing_urls:  # Skip if already in pickle
                continue
            
            publish_date = doc.metadata.get('publish_date')
            if not publish_date:
                continue  # Skip articles with no date. The links that did not have a date were not articles. 
            
            new_articles.append({
                'title': doc.metadata.get('title', ''),
                'url': article_url,
                'text': doc.page_content,
                'category': category,
                'date': publish_date.strftime("%B %d %Y"),
                'author(s)': doc.metadata.get('authors')
                })

            self.existing_urls.add(article_url)  # Add to the existing URLs set
            
        '''
        # Print the new articles added for clarity
        if new_articles:
            print(f"New articles added: {len(new_articles)}")
        '''
        return new_articles

'''
if __name__ == "__main__":
    scraper = NewsScraper()
    results = scraper.scrape_news()
    print(results['date'])
    df = pd.DataFrame(results)
    print(df.head())
    df.to_csv('Scraped_articles_new.csv', index=False)
'''
