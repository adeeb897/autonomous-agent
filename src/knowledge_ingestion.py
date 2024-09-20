import requests

class KnowledgeIngestionPipeline:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_resources(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(self.api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def store_resources(self, data, file_path='data/resources.json'):
        with open(file_path, 'w') as file:
            json.dump(data, file)

# Example usage
# api_url = 'https://api.example.com/educational_resources'
# api_key = 'your_api_key'
# pipeline = KnowledgeIngestionPipeline(api_url, api_key)
# data = pipeline.fetch_resources()
# pipeline.store_resources(data)
