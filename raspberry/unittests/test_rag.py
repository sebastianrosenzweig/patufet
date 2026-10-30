import unittest
from patufet.rag import generate_response

class TestRAG(unittest.TestCase):
    def test_reasoning(self):
        response = generate_response("Qui era el 130è President de la Generalitat de Catalunya?")

        self.assertIn("Carles Puigdemont", response)

    def test_empty_query(self):
        response = generate_response("")
        self.assertEqual(response, "No entenc la pregunta. Pots repetir, si us plau?")
