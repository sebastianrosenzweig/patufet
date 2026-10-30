import unittest
from patufet.translation import translate

class TestTranslation(unittest.TestCase):
    def test_translate(self):
        text_ca = "El cel és blau."
        text_en = "The sky is blue."

        result_en = translate(text_ca, "Catalan", "English")
        result_ca = translate(text_en, "English", "Catalan")

        self.assertEqual(result_en, text_en)
        self.assertEqual(result_ca, text_ca)
