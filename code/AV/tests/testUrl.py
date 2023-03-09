from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AV.views import homepage


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare l'applicazione Analizza Vocabolario"""

    def homepage_URL_is_resolved(self):
        """Verifica che l'url assegnato alla pagina di homepage
        effettivamente indirizza alla pagina di homepage
        """
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)