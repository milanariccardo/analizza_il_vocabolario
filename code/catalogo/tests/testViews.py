from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.db import models

from catalogo.models import Testo


class TestView(TestCase):
    """Classe che verifica il corretto funzionamento delle views (viste)
    dell'applicazione Catalogo."""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test"""
        self.insert_text = reverse('catalogo:insert-text')
        self.search_text = reverse('catalogo:search')
        self.visualize_text = reverse('catalogo:visualizza-text', args=['1'])
        self.search_text_compare = reverse('catalogo:text-search-compare')
        self.compare_text = reverse('catalogo:text-compare', args=['1', '2'])
        self.global_statistics = reverse('catalogo:statistiche_globali')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        self.client = Client()

    def testVisualizeText(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina dell'analisi del testo sia 200 (buon fine), nel caso in cui il login
        sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.visualize_text)
        self.assertEqual(response.status_code, 200)

    def testVisualizeTextRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina dell'analisi del testo sia 302 (redirect), nel caso di mancato login.
        Questo perchè per visualizzare l'analisi del testo è richiesto il login."""
        response = self.client.get(self.visualize_text)
        self.assertEqual(response.status_code, 302)

    def testInsertText(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina dell'analisi del testo sia 200 (buon fine), nel caso in cui il login
        sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.insert_text)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/insertText.html')

    def testInsertTextRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina dell'analisi del testo sia 302 (redirect), nel caso di mancato login.
        Questo perchè per inserire un testo è richiesto il login."""
        response = self.client.get(self.insert_text)
        self.assertEqual(response.status_code, 302)

    def testSearchText(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di ricerca del testo sia 200 (buon fine), nel caso in cui il login
        sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.search_text)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/searchText.html')

    def testSearchTextRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di ricerca del testo sia 302 (redirect), nel caso di mancato login.
        Questo perchè per ricercare un testo è richiesto il login."""
        response = self.client.get(self.search_text)
        self.assertEqual(response.status_code, 302)

    def testSearchCompareText(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di ricerca dei testi da comparare sia 200 (buon fine),
        nel caso in cui il login sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.search_text_compare)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/searchCompareText.html')

    def testSearchCompareTextRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di selezione dei testi per la comparazione sia 302 (redirect),
        nel caso di mancato login. Questo perchè per comparare un testo è richiesto
        il login."""
        response = self.client.get(self.search_text_compare)
        self.assertEqual(response.status_code, 302)

    def testCompareTextRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina di comparazione sia 302 (redirect), nel caso di mancato login.
        Questo perchè per visualizzare l'analisi del testo è richiesto il login."""
        response = self.client.get(self.compare_text)
        self.assertEqual(response.status_code, 302)

    def testGlobalStatistics(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina delle statistiche sia 200 (buon fine), nel caso in cui il login
        sia stato effettuato correttamente."""
        self.logged_in = self.client.login(username='testuser', password='password')
        response = self.client.get(self.search_text_compare)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/searchCompareText.html')

    def testGlobalStatisticsRedirect(self):
        """Verifica che la risposta del server al tentativo di richiesta GET
        della pagina delle statistiche sia 302 (redirect), nel caso di mancato login.
        Questo perchè per visualizzare l'analisi del testo è richiesto il login."""
        response = self.client.get(self.global_statistics)
        self.assertEqual(response.status_code, 302)
