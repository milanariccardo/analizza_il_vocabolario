from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

class TestView(TestCase):
    """Classe utilizzata per testare le view (viste) dell'applicazione
    di Analizza Vocabolario"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test"""
        self.homepage = reverse('homepage')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        self.client = Client()



    def test_homepage_with_redirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di Homepage sia 302 (redirect), nel caso di mancato login.
        Questo perchè per visualizzare l'homepage è richiesto il login."""
        response = self.client.get(self.homepage)
        self.assertEqual(response.status_code, 302)


    def test_homepage(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di Homepage sia 200 (buon fine), nel caso in cui il login
        sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.homepage)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

