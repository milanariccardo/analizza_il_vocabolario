from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import SignUp, BlacklistView


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare l'url dell'applicazione account"""

    def testSignupURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina di SignUp effettivamente indirizza alla pagina di registrazione."""
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUp)

    def testBlacklistURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina della blacklist effettivamente indirizza alla pagina della
        blacklist."""
        url = reverse('blacklist')
        self.assertEquals(resolve(url).func.view_class, BlacklistView)
