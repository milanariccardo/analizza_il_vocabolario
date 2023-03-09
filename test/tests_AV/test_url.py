from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AV.views import homepage
from catalogo.views import TextAdd


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare l'applicazione Analizza Vocabolario"""

    def test_list_url_is_resolved(self):
        """Verifica che l'url assegnato alla pagina di homepage
        effettivamente indirizza alla pagina di homepage
        """
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)