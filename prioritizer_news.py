IMPORTANT_KEYWORDS = ["breaking news", "exclusive", "just in", "critical update", 
                      "developing", "news flash", "state of emergency"]

def prioritize_articles(articles, keywords=None):
    if keywords is None:
        keywords = IMPORTANT_KEYWORDS

    prioritized = []
    for article in articles:
        text = (article.get('title', '') + " " + article.get('text', '')).lower()
        frequency = article.get('frequency', 1)

        # Keyword score
        article['keywords'] = [kw for kw in keywords if kw in text]
        keyword_score = len(article['keywords'])

        # Final priority score, Giving keyword more priority
        score = keyword_score + frequency
        article['priority_score'] = score
        prioritized.append(article)

    # Sort descending by score
    prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
    return prioritized