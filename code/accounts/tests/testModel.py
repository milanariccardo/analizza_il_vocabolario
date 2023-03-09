from django.contrib.auth.models import User
from django.test import TestCase

from textManipulation.textAnalyzer import TextAnalyzer
from accounts.models import Blacklist


class TestModels(TestCase):
    """Classe utilizzata per testare i models dell'applicazione accounts"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        vengono creati due users che verranno utilizzati nel corso dei test"""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

        self.user1 = User.objects.create(username='testuser1')
        self.user1.set_password('password')
        self.user1.save()

    @staticmethod
    def insertBlacklistWord(user, word):
        """Metodo utilizzato per inserire una parola nella blacklist di un utente nel database
        :return: riferimento alla parola inserita nel database"""
        blacklistWord = Blacklist.objects.create(
            utente=user,
            parola=word
        )
        blacklistWord.success = True
        blacklistWord.T = TextAnalyzer(word)
        blacklistWord.save()
        return blacklistWord

    def testCorrectInsertion(self):
        """Verifica un inserimento corretto"""
        word = self.insertBlacklistWord(self.user, 'prova')
        word = Blacklist.objects.last()

        self.assertTrue(isinstance(word, Blacklist))

    def testTwoUserOneWord(self):
        """Verifica che due utenti possono avere una stessa parola nella blacklist"""
        word = self.insertBlacklistWord(self.user, 'prova')
        word1 = self.insertBlacklistWord(self.user1, 'prova')

        self.assertTrue(isinstance(word, Blacklist))
        self.assertTrue(isinstance(word1, Blacklist))
