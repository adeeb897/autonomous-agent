import os
import requests
from tempfile import TemporaryDirectory
from dev_tools import GitRepo
from langchain_community.agent_toolkits import FileManagementToolkit
from detoxify import Detoxify

class KnowledgeIngestion:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_toolkit = FileManagementToolkit(root_dir=root_dir)
        self.repo = GitRepo(root_dir)

    def fetch_resource(self, url, filename):
        """Fetch a resource from a URL and save it to the workspace."""
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(self.root_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
        else:
            raise Exception(f"Failed to fetch resource from {url}")

    def fetch_api_data(self, api_url, params=None):
        """Fetch data from an API endpoint."""
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from API {api_url}")

    def filter_content(self, file_path):
        """Filter content to exclude low-quality or harmful information."""
        filtered_file_path = os.path.join(self.root_dir, "filtered_" + os.path.basename(file_path))
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Enhanced content filtering logic
        # Use Detoxify to check for toxicity in the content
        results = Detoxify('original').predict(content)
        if results['toxicity'] > 0.5 or results['severe_toxicity'] > 0.5 or results['obscene'] > 0.5 or results['threat'] > 0.5 or results['insult'] > 0.5 or results['identity_attack'] > 0.5:
            raise ValueError("Content is considered harmful and has been filtered out.")
        
        with open(filtered_file_path, 'w') as f:
            f.write(content)
        return filtered_file_path

    def preprocess_data(self, data):
        """Preprocess fetched data."""
        # Implement preprocessing logic here
        return data

    def ingest_resource(self, url, filename):
        """Fetch, filter, and save a resource to the knowledge base."""
        file_path = self.fetch_resource(url, filename)
        filtered_path = self.filter_content(file_path)
        return filtered_path

    def ingest_api_data(self, api_url, params=None):
        """Fetch, preprocess, and save API data to the knowledge base."""
        data = self.fetch_api_data(api_url, params=params)
        preprocessed_data = self.preprocess_data(data)
        # Save preprocessed data to file or database
        return preprocessed_data

# Example usage
if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        ingestion = KnowledgeIngestion(temp_dir)
        resource_url = "https://example.com/resource.pdf"
        filename = "resource.pdf"
        try:
            ingested_path = ingestion.ingest_resource(resource_url, filename)
            print(f"Resource ingested at: {ingested_path}")
        except ValueError as e:
            print(e)

        api_url = "https://api.example.com/data1"
        try:
            api_data = ingestion.ingest_api_data(api_url)
            print(f"API data ingested: {api_data}")
        except Exception as e:
            print(e)
