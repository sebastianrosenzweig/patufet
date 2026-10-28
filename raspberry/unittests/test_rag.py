import unittest
from rag import generate_response

class TestRAG(unittest.TestCase):
    def test_reasoning(self):
        response = generate_response("Qui era el 130è President de la Generalitat de Catalunya?")
        assert "Carles Puigdemont" in response

if __name__ == "__main__":
    unittest.main()
