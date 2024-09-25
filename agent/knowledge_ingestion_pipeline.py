import requests
from textblob import TextBlob

class KnowledgeIngestionPipeline:
    def __init__(self, sources):
        self.sources = sources

    def fetch_resources(self):
        resources = []
        for source in self.sources:
            response = requests.get(source)
            if response.status_code == 200:
                resources.append(response.text)
        return resources

    def filter_content(self, content):
        filtered_content = []
        for item in content:
            if not self.is_toxic(item) and not self.is_biased(item):
                filtered_content.append(item)
        return filtered_content

    @staticmethod
    def is_toxic(text):
        # Placeholder for toxicity analysis
        analysis = TextBlob(text)
        return analysis.sentiment.polarity < -0.5

    @staticmethod
    def is_biased(text):
        # Placeholder for bias detection
        analysis = TextBlob(text)
        return 'bias' in analysis.lower()