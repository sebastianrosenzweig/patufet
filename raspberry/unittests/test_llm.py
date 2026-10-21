import unittest
from llm import get_llm_response

class TestLLM(unittest.TestCase):
    def test_reasoning(self):
        get_llm_response("Quants anys té Carles Puigdemont?")

if __name__ == "__main__":
    unittest.main()
