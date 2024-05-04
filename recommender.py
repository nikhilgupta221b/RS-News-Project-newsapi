# recommender.py
import numpy as np
import requests

class ThompsonSamplingNewsRecommender:
    def __init__(self, categories, api_key):
        self.categories = categories
        self.api_key = api_key
        self.alpha = {category: 1 for category in categories}
        self.beta = {category: 1 for category in categories}

    def sample_preferences(self):
        sampled_values = {category: np.random.beta(self.alpha[category], self.beta[category])
                          for category in self.categories}
        return sampled_values

    def get_top_categories(self, n=3):
        preferences = self.sample_preferences()
        top_categories = sorted(preferences, key=preferences.get, reverse=True)[:n]
        return top_categories

    def update_initial_preferences(self, category, outcome):
        if outcome == 'like':
            self.alpha[category] += 3
        elif outcome == 'dislike':
            self.beta[category] += 3

    def update_preferences(self, category, outcome):
        if outcome == 'like':
            self.alpha[category] += 1
        elif outcome == 'dislike':
            self.beta[category] += 1

    def fetch_news(self, categories):
        news = {}
        url = 'https://newsapi.org/v2/top-headlines'
        headers = {'Authorization': 'Bearer ' + self.api_key}
        for category in categories:
            params = {'category': category, 'country': 'in', 'pageSize': 3}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                news[category] = [article['title'] for article in articles]
            else:
                news[category] = ["Failed to fetch news"]
        return news
