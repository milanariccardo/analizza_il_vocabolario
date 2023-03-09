from django.contrib.auth.models import User
from django.test import TestCase

from textManipulation.textAnalyzer import TextAnalyzer
from accounts.forms import BlacklistForm


def corretto(testo):
    """Metodo che controlla la correttezza della parola inserito nel form.
    :param testo: testo da inserire nel database
    :return: True se il testo è corretto, False altrimenti"""
    try:
        T = TextAnalyzer(testo)
        return True
    except AssertionError:
        return False


class FormTest(TestCase):
    """Classe utilizzata per testare il form di inserimento delle parole nella blacklist"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test"""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    @staticmethod
    def setForm(word):
        return BlacklistForm(data={
            'parola': word
        })

    def testGoodData(self):
        """Metodo che verifica che il form sia valido se viene inserita una parola nel giusto formato"""
        form = self.setForm('prova')
        self.assertTrue(form.is_valid())

    def testNoData(self):
        """Metodo che verifica che il form sia non valido se non sono stati inseriti dati"""
        form = BlacklistForm(data={})
        self.assertFalse(form.is_valid())

    def testNoTextData(self):
        """Metodo che verifica se sono stati inseriti solo spazi, quindi l'invalidità dei dati inseriti"""
        form = self.setForm(' ')
        self.assertFalse(corretto(form.data['parola']))

    def testCleanPreDirtyData(self):
        """Metodo che verifica la validità del form se viene inserita una parola con caratteri di interpunzione"""
        form = self.setForm(',,,,.prova')
        self.assertTrue(corretto(form.data['parola']))

    def testCleanPostDirtyData(self):
        """Metodo che verifica la validità del form se viene inserita una parola con caratteri di interpunzione"""
        form = self.setForm('prova...-..-,')
        self.assertTrue(corretto(form.data['parola']))

    def testOnlyPunctuationData(self):
        """Metodo che verifica la non validità del form se la parola è composta da soli segni di interpunzione"""
        form = self.setForm(',,,,.')
        self.assertFalse(corretto(form.data['parola']))
