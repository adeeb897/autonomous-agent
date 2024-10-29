"""
This module provides functionality for knowledge ingestion, including fetching resources from URLs,
filtering content to exclude low-quality or harmful information, and saving the filtered content to
a knowledge base.
"""

import os
from tempfile import TemporaryDirectory

import requests
from langchain_community.agent_toolkits import FileManagementToolkit
from detoxify import Detoxify
from textblob import TextBlob
import logging

class KnowledgeIngestion:
    """A class to manage knowledge ingestion, including fetching and filtering content."""

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_toolkit = FileManagementToolkit(root_dir=root_dir)
        logging.basicConfig(level=logging.INFO)

    def fetch_resource(self, url, filename):
        """Fetch a resource from a URL and save it to the workspace."""
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return self._save_resource_to_workspace(response, filename)
        raise RuntimeError(f"Failed to fetch resource from {url}")

    def _save_resource_to_workspace(self, response, filename):
        """Save the fetched resource to the workspace."""
        file_path = os.path.join(self.root_dir, filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path

    def filter_content(self, file_path):
        """Filter content to exclude low-quality or harmful information."""
        content = self._read_content(file_path)
        self._validate_content(content)
        return self._save_filtered_content(content, file_path)

    def _read_content(self, file_path):
        """Read the content from the file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _validate_content(self, content):
        """Validate the content for toxicity, bias, and misinformation."""
        if self.is_toxic(content):
            logging.info("Content is toxic and has been filtered out.")
            raise ValueError("Content is considered harmful and has been filtered out.")
        if self.is_biased(content):
            logging.info("Content is biased and has been filtered out.")
            raise ValueError("Content is considered harmful and has been filtered out.")
        if self.is_misinformation(content):
            logging.info("Content contains misinformation and has been filtered out.")
            raise ValueError("Content is considered harmful and has been filtered out.")

    def _save_filtered_content(self, content, file_path):
        """Save the filtered content to a new file."""
        filtered_file_path = os.path.join(
            self.root_dir, "filtered_" + os.path.basename(file_path)
        )
        with open(filtered_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return filtered_file_path

    @staticmethod
    def is_toxic(text):
        # Use Detoxify to check for toxicity in the content
        results = Detoxify("original").predict(text)
        is_toxic = (
            results["toxicity"] > 0.5 or results["severe_toxicity"] > 0.5 or
            results["obscene"] > 0.5 or results["threat"] > 0.5 or
            results["insult"] > 0.5 or results["identity_attack"] > 0.5
        )
        return is_toxic

    @staticmethod
    def is_biased(text):
        # Placeholder for bias detection
        analysis = TextBlob(text)
        return 'bias' in analysis.lower()

    @staticmethod
    def is_misinformation(text):
        # Placeholder for misinformation detection
        return 'misinformation' in text.lower()

    def ingest_resource(self, url, filename):
        """Fetch, filter, and save a resource to the knowledge base."""
        file_path = self.fetch_resource(url, filename)
        return self.filter_content(file_path)


# Example usage
if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        INGESTION = KnowledgeIngestion(temp_dir)
        RESOURCE_URL = "https://example.com/resource.pdf"
        FILENAME = "resource.pdf"
        try:
            ingested_path = INGESTION.ingest_resource(RESOURCE_URL, FILENAME)
            print(f"Resource ingested at: {ingested_path}")
        except ValueError as e:
            print(e)
