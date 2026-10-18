import unittest
from unittest.mock import patch, MagicMock
from llm import get_llm_response

class TestLLM(unittest.TestCase):
    @patch('llm.get_llm_instance')
    def test_llm_response_with_mock(self, mock_llm_instance):
        # Mock the LLM instance
        mock_instance = MagicMock()
        mock_instance.create_completion.return_value = {
            "predictions": [{"text": "Bé, estic molt bé, gràcies! I tu?"}]
        }
        mock_llm_instance.return_value = mock_instance

        result = get_llm_response("Com estàs?")
        self.assertIn("Bé, estic molt bé", result)

    def test_llm_response_empty_input(self):
        # Test with empty string
        result = get_llm_response("")
        self.assertIn("No entenc la consulta", result)

if __name__ == "__main__":
    unittest.main()
