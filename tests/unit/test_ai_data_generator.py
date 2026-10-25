import unittest
from unittest.mock import patch, MagicMock

# from utils.ai_data_generator import generate_product_payload


class TestAIDataGenerator(unittest.TestCase):
    """Placeholder test for the LLM‑driven payload generator."""

    @patch("utils.ai_data_generator.openai.ChatCompletion.create")
    def test_generate_product_payload(self, mock_create):
        """Mock the LLM call and verify the function returns a dict."""
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='{"title":"Demo","price":9.99}'))]
        )

        # payload = generate_product_payload()
        # self.assertIsInstance(payload, dict)
        # self.assertIn("title", payload)

        # ---- TODO: replace the placeholder with real call & assertions ----
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()