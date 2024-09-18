import os
import requests
from tempfile import TemporaryDirectory
from dev_tools import GitRepo
from langchain_community.agent_toolkits import FileManagementToolkit

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

    def filter_content(self, file_path):
        """Filter content to exclude low-quality or harmful information."""
        filtered_file_path = os.path.join(self.root_dir, "filtered_" + os.path.basename(file_path))
        # Placeholder for content filtering logic
        # For demonstration, we will just copy the original file content to the filtered file
        with open(file_path, 'r') as f:
            content = f.read()
        # Here you can add actual filtering logic such as toxicity analysis, bias detection, etc.
        # For now, we will assume the content is clean and write it to the filtered file
        with open(filtered_file_path, 'w') as f:
            f.write(content)
        return filtered_file_path

    def ingest_resource(self, url, filename):
        """Fetch, filter, and save a resource to the knowledge base."""
        file_path = self.fetch_resource(url, filename)
        filtered_path = self.filter_content(file_path)
        return filtered_path

# Example usage
if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        ingestion = KnowledgeIngestion(temp_dir)
        resource_url = "https://example.com/resource.pdf"
        filename = "resource.pdf"
        ingested_path = ingestion.ingest_resource(resource_url, filename)
        print(f"Resource ingested at: {ingested_path}")