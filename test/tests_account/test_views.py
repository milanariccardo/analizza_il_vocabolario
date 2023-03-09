from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from templates.registration import *

class TestView(TestCase):
    """Classe utilizzata per testare le view (viste)
    dell'applicazione account"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test"""
        self.client = Client()
        self.var = reverse('signup')


    def test_signup(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di SignUp sia 200 (buon fine)"""
        response = self.client.get(self.var)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
