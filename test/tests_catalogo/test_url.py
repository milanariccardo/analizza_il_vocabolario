from django.test import SimpleTestCase
from django.urls import reverse, resolve
from catalogo.views import TextAdd, search, TextView


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare l'applicazione di Catalogo"""

    def test_list_url_is_resolved(self):
        """Verifica che l'url assegnato alla pagina di inserimento del testo
        effettivamente indirizza alla pagina di inserimento del testo."""
        url = reverse('catalogo:insert-text')
        self.assertEquals(resolve(url).func.view_class, TextAdd)

    def test_search_URL(self):
        """Verifica che l'url assegnato alla pagina di ricerca del testo
        effettivamente indirizza alla pagina di ricerca del testo."""
        url = reverse('catalogo:search')
        self.assertEquals(resolve(url).func, search)

    def test_visualize_URL(self):
        """Verifica che l'url assegnato alla pagina del risultato di un'analisi
        di un testo effettivamente indirizza alla pagina in questione."""
        url = reverse('catalogo:visualizza-text', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TextView)


