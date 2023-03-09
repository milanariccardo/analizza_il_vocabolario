from django.test import TestCase
from translation.translate import Translate
import re


class TestModels(TestCase):
    """Classe utilizzata per testare la traduzione"""

    def testInvalidWord(self):
        """Metodo che prende in ingresso una parola inesistente e ritorna la stessa parola (nessuna traduzione)"""
        translatedWord = Translate(['opodo'], 'en')
        self.assertEqual(['opodo'], translatedWord.get_translated_words())

    def testPunctuationWord(self):
        """Metodo che prende in ingresso della punteggiatura e ritorna la punteggiatura inserita (nessuna traduzione)"""
        translatedWord = Translate(['...,.,.'], 'en')
        self.assertEqual(['...,.,.'], translatedWord.get_translated_words())

    def testNumbers(self):
        """Metodo che prende in ingresso dei numeri e ritorna i numeri inseriti (nessuna traduzione)"""
        translatedWord = Translate(['12345'], 'de')
        self.assertEqual(['1 2 3 4 5'], translatedWord.get_translated_words())

    def testCiaoInEnglish(self):
        """Metodo che prende in ingresso una parola e ne ritorna la traduzione in inglese"""
        translatedWord = Translate(['ciao'], 'en')
        self.assertEqual(['hi'], translatedWord.get_translated_words())

    def testCiaoInGerman(self):
        """Metodo che prende in ingresso una parola e ne ritorna la traduzione in tedesco"""
        translatedWord = Translate(['ciao'], 'de')
        self.assertEqual(['hallo'], translatedWord.get_translated_words())
