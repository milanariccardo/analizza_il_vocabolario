from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from catalogo.models import Testo, Token
from textManipulation.textAnalyzer import TextAnalyzer
from django.db import IntegrityError


class TestModels(TestCase):
    """Classe utilizzata per testare i models dell'applicazione Catalogo"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test"""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def createText(self):
        """Metodo utilizzato per creare un testo da inserire nel database in fase di testing
        :return: riferimento al testo creato e inserito nel database"""
        testo = Testo.objects.create(
            titolo="Coronavirus 2020",
            autore="Giovanni Mucci",
            tipo="Tema Scolastico",
            descrizione="prima media",
            pubblicatore=self.user
        )
        testo.success = True
        testo.text_complete = 'afdasdf'
        testo.T = TextAnalyzer(testo.text_complete)
        testo.save()
        return testo

    @staticmethod
    def createToken(text):
        """Metodo utilizzato per creare un token da inserire nel database in fase di testing
        return: riferimento al token creato e inserito nel database"""
        return Token.objects.create(
            testo=text,
            parola="prova",
            frequenza="3"
        )

    def testStringRepresentation(self):
        """Metodo che verifica la corretta rappresentazione di un record della tabella Testo,
        nel momento in cui lo si stampa."""
        text = self.createText()
        text = Testo.objects.last()

        self.assertEqual(text.__str__(), 'id: 1 - Titolo: Coronavirus 2020 ')

    def testNoRepetitionToken(self):
        """Verifica che può esistere lo stesso token in testi diversi"""
        text = self.createText()
        text = Testo.objects.last()

        text1 = self.createText()
        text1 = Testo.objects.last()

        token = self.createToken(text)
        token1 = self.createToken(text1)

        self.assertTrue(isinstance(token, Token))
        self.assertTrue(isinstance(token1, Token))

    def testUniqueTokenInText(self):
        """Verifica che un token deve essere presente una sola volta nel testo"""
        result = "No error"
        text = self.createText()
        text = Testo.objects.last()
        token = self.createToken(text)

        try:
            token1 = self.createToken(text)
        except IntegrityError as error:
            result = "Error"

        self.assertEqual(result, "Error")
