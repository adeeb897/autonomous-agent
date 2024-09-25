import unittest
from agent.knowledge_ingestion_pipeline import KnowledgeIngestionPipeline

class TestKnowledgeIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = KnowledgeIngestionPipeline(sources=["http://example.com/resource1", "http://example.com/resource2"])

    def test_fetch_resources(self):
        resources = self.pipeline.fetch_resources()
        self.assertIsInstance(resources, list)

    def test_filter_content(self):
        content = ["This is a good text", "This is a toxic text"]
        filtered_content = self.pipeline.filter_content(content)
        self.assertEqual(len(filtered_content), 1)

    def test_is_toxic(self):
        self.assertTrue(self.pipeline.is_toxic("This is a toxic text"))
        self.assertFalse(self.pipeline.is_toxic("This is a good text"))

    def test_is_biased(self):
        self.assertTrue(self.pipeline.is_biased("This text is biased"))
        self.assertFalse(self.pipeline.is_biased("This text is neutral"))

if __name__ == '__main__':
    unittest.main()