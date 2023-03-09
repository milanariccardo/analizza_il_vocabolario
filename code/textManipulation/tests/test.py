# -*- coding: utf-8 -*-
from django.test import TestCase
from textManipulation.textAnalyzer import TextAnalyzer


class TextAnalyzerTestBase(TestCase):
    """Classe che verifica il corretto funzionamento della manipolazione nel caso in cui
    non ci siano parole composte."""

    # Testo senza parole composte
    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno testo e un'istanza della classe TextAnalyzer che verrà utilizzato nel corso del test"""
        self.text = "prova testo. . testo# , ciao"
        self.T = TextAnalyzer(self.text)

    def testInit(self):
        """Test che verifica se l'oggetto creato sia effettivamente un'istanza di TextAnalyzer"""
        self.assertTrue(isinstance(self.T, TextAnalyzer))

    def testTokenizer(self):
        """Test che verifica che il resultato della manipolazione effettuata sul testo di prova sia corretto."""
        expected = {'prova': 1, 'testo': 2, 'ciao': 1}
        self.assertEqual(self.T.tokenizer(self.text), expected)

    def testTextComplexity(self):
        """Test che verifica che la complessità calcolata sul testo di prova sia corretta."""
        self.assertAlmostEqual(self.T.textComplexity(), 0.375, delta=1)

    def testGetNumParole(self):
        """Test che verifica che il numero di parole calcolato sul testo di prova sia corretto."""
        expected = 4
        self.assertEqual(self.T.getTotalNumberOfTerms(), expected)

    def testGetCardinality(self):
        """Test che verifica che la cardinalità del vocabolario del testo di prova sia corretta."""
        expected = 3
        self.assertEqual(self.T.getCardinality(), expected)

    def testGetLexicalDensity(self):
        """Test che verifica che la densità lessicale calcolata sul testo di prova sia corretta."""
        expected = 0.75
        self.assertEqual(self.T.getLexicalDensity(), expected)


class TextAnalyzerTestComposed(TestCase):
    """Classe che verifica il corretto funzionamento della manipolazione nel caso in cui
      ci siano parole composte."""

    # Testo con parole composte e numeri
    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno testo e un'istanza della classe TextAnalyzer che verrà utilizzato nel corso del test"""
        self.text = "parole composte tipo anti-nebbia 435"
        self.T = TextAnalyzer(self.text)

    def testInit(self):
        """Test che verifica se l'oggetto creato sia effettivamente un'istanza di TextAnalyzer"""
        self.assertTrue(isinstance(self.T, TextAnalyzer))

    def testTokenizer(self):
        """Test che verifica che il resultato della manipolazione effettuata sul testo di prova sia corretto."""
        expected = {'parole': 1, 'composte': 1, 'tipo': 1, 'anti': 1, 'nebbia': 1, '435': 1}
        self.assertEqual(self.T.tokenizer(self.text), expected)

    def testTextComplexity(self):
        """Test che verifica che la complessità calcolata sul testo di prova sia corretta."""
        self.assertAlmostEqual(self.T.textComplexity(), 1.3, delta=1)

    def testGetNumParole(self):
        """Test che verifica che il numero di parole calcolato sul testo di prova sia corretto."""
        expected = 6
        self.assertEqual(self.T.getTotalNumberOfTerms(), expected)

    def testGetCardinality(self):
        """Test che verifica che la cardinalità del vocabolario del testo di prova sia corretta."""
        expected = 6
        self.assertEqual(self.T.getCardinality(), expected)

    def testGetLexicalDensity(self):
        """Test che verifica che la densità lessicale calcolata sul testo di prova sia corretta."""
        expected = 1
        self.assertEqual(self.T.getLexicalDensity(), expected)


class TextAnalyzerTestMalformed(TestCase):
    """Classe che verifica lo scorretto funzionamento della manipolazione nel caso in cui
      il testo sia malformato."""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno testo malformato e un'istanza della classe TextAnalyzer
        che verrà utilizzato nel corso del test"""
        self.text = "!"
        self.error = "Nessun errore"

    def testInit(self):
        """Test che verifica se l'oggetto creato sia effettivamente malformato."""
        try:
            self.T = TextAnalyzer(self.text)
        except AssertionError:
            self.error = "Testo malformato"

        self.assertEqual(self.error, "Testo malformato")


class TextAnalyzerTestCompare(TestCase):
    """Classe che compara la complessità di due testi."""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        vegono creati due testi e due istanze della classe TextAnalyzer
        che verranno utilizzate nel corso del test"""
        self.text = "D'in su la vetta della torre antica, Passero solitario, alla campagna Cantando vai finchè non more il giorno; Ed erra l'armonia per questa valle."
        self.text2 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
        self.T = TextAnalyzer(self.text)
        self.T2 = TextAnalyzer(self.text2)

    def testCompareComplexity(self):
        """Test che verifica che la corretta comparazione tra i due testi."""
        self.assertTrue(self.T.textComplexity() > self.T2.textComplexity())
