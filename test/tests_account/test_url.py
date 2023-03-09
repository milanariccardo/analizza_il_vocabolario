from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import SignUp


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare l'url dell'applicazione account"""

    def test_list_url_is_resolved(self):
        """Verifica che l'url assegnato alla pagina di SignUp
        effettivamente indirizza alla pagina di registrazione
        """

        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUp)