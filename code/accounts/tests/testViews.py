from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from templates.registration import *


class TestView(TestCase):
    """Classe utilizzata per testare le view (viste) dell'applicazione account"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test"""
        self.client = Client()
        self.blacklist = reverse('blacklist')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def testSignup(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di SignUp sia 200 (buon fine)"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def testBlacklist(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina della blacklist sia 200 (buon fine),
        nel caso in cui il login sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.blacklist)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/blacklist.html')

    def testBlacklistRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina blacklist sia 302 (redirect) nel caso di mancato login.
        Questo perchè per visualizzare la blacklist è richiesto il login."""
        response = self.client.get(reverse('blacklist'))
        self.assertEqual(response.status_code, 302)
