from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from catalogo.models import Testo, Token
from catalogo.forms import TextCrispyForm, TextCrispyFormComplete
from Text_manipulation.TextAnalyzer import TextAnalyzer


def corretto(testo):
    """Metodo che controlla la correttezza del testo inserito nel form.
    :param testo: testo da inserire nel database
    :return: True se il testo è corretto, False altrimenti"""
    try:
        T = TextAnalyzer(testo)
        return True
    except AssertionError:
        return False


class FormTest(TestCase):
    """Classe utilizzata per testare il form di inserimento di tutte le informazioni
    relative a un testo"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test"""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def test_valid_data(self):
        """Metodo che verifica se i dati inseriti sono validi"""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate"
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(corretto(form.data['text_complete']))
        self.assertTrue(corretto(form.data['titolo']))
        self.assertTrue(corretto(form.data['autore']))

    def test_no_data(self):
        """Metodo che verifica se i dati non siano stati inseriti,
        quindi la loro invalidità"""
        form = TextCrispyForm(data={
        })

        self.assertFalse(form.is_valid())

    def test_no_title_data(self):
        """Metodo che verifica l'invalidità se il titolo non è stato inserito
        nel form (obbligatorio)."""
        form = TextCrispyFormComplete(data={
            'titolo': ' ',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate"
        })
        self.assertFalse(form.is_valid())

    def test_no_autore_data(self):
        """Metodo che verifica l'invalidità se l' autore non è stato inserito
        nel form (obbligatorio). """
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': ' ',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate"
        })
        self.assertFalse(form.is_valid())

    def test_no_text_data(self):
        """Metodo che verifica l'invalidità se il testo non è stato inserito
        nel form (obbligatorio). """
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': " "
        })
        self.assertFalse(form.is_valid())

    def test_invalid_title_data(self):
        """Metodo che verifica l'invalidità se il titolo non è stato inserito
        correttamente (presenza di soli segni di punteggitura/caratteri speciali )."""
        form = TextCrispyFormComplete(data={
            'titolo': '. //**/*////',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertFalse(corretto(form.data['titolo']))

    def test_valid_title_data(self):
        """Metodo che verifica la validità se il titolo è stato inserito
        correttamente (presenza di almeno di un carattere alfanumerico)."""
        form = TextCrispyFormComplete(data={
            'titolo': '.a',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertTrue(corretto(form.data['titolo']))

    def test_valid_title_number_data(self):
        """Metodo che verifica la validità se il titolo è stato inserito
        correttamente (presenza di soli caratteri numerici)."""
        form = TextCrispyFormComplete(data={
            'titolo': '4424242 ',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertTrue(corretto(form.data['titolo']))

    ######## TEST AUTORE ##############
    def test_invalid_author_data(self):
        """Metodo che verifica l'invalidità se l'autore non è stato inserito
        correttamente (presenza di soli segni di punteggitura/caratteri speciali )."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': '. //**/*////',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertFalse(corretto(form.data['autore']))

    def test_valid_author_data(self):
        """Metodo che verifica la validità se l'autore è stato inserito
        correttamente (presenza di almeno di un carattere alfanumerico)."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': '.s',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertTrue(corretto(form.data['autore']))

    def test_valid_author_number_data(self):
        """Metodo che verifica la validità se l'autore è stato inserito
        correttamente (presenza di soli caratteri numerici)."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': '4424242',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "La mafia uccide solo d'estate "
        })
        self.assertTrue(corretto(form.data['autore']))

    ######## TEST TESTO ##############
    def test_invalid_text_complete_data(self):
        """Metodo che verifica l'invalidità se il testo non è stato inserito
        correttamente (presenza di soli segni di punteggitura/caratteri speciali )."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': ". //**/*////"
        })
        self.assertFalse(corretto(form.data['text_complete']))

    def test_valid_text_complete_data(self):
        """Metodo che verifica la validità se il testo è stato inserito
        correttamente (presenza di almeno di un carattere alfanumerico)."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "..La"
        })
        self.assertTrue(corretto(form.data['text_complete']))

    def test_valid_text_complete_number_data(self):
        """Metodo che verifica la validità se il testo è stato inserito
        correttamente (presenza di soli caratteri numerici)."""
        form = TextCrispyFormComplete(data={
            'titolo': 'Gomorra',
            'autore': 'Saviano',
            'tipo': '1',
            'descrizione': '',
            'text_complete': "54343"
        })
        self.assertTrue(corretto(form.data['text_complete']))
