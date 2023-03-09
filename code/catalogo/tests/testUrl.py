from django.test import SimpleTestCase
from django.urls import reverse, resolve
from catalogo.views import TextAdd, search, TextView, TextSearchCompare, GlobalStatView, ViewCompare


class TestUrls(SimpleTestCase):
    """Classe utilizzata per testare gli url dell'applicazione Catalogo"""

    def testInsertTextURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina di inserimento del testo
        effettivamente indirizza alla pagina di inserimento del testo."""
        url = reverse('catalogo:insert-text')
        self.assertEquals(resolve(url).func.view_class, TextAdd)

    def testSearchTextURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina di ricerca del testo
        effettivamente indirizza alla pagina di ricerca del testo."""
        url = reverse('catalogo:search')
        self.assertEquals(resolve(url).func, search)

    def testVisualizeTextURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina del risultato di un'analisi
        di un testo effettivamente indirizza alla pagina in questione."""
        url = reverse('catalogo:visualizza-text', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TextView)

    def testCompareTextsURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina per cercare due testi da comparare
        effettivamente indirizza alla pagina per cercare due testi da comparare"""
        url = reverse('catalogo:text-search-compare')
        self.assertEquals(resolve(url).func, TextSearchCompare)

    def testCompareTextURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina di comparazione
        di due testi effettivamente indirizza alla pagina in questione."""
        url = reverse('catalogo:text-compare', args=['1', '2'])
        self.assertEquals(resolve(url).func.view_class, ViewCompare)

    def testGlobalStatisticsURLIsResolved(self):
        """Verifica che l'url assegnato alla pagina per la visualizzazione delle
        statistiche globali effettivamente indirizza alla pagina in questione."""
        url = reverse('catalogo:statistiche_globali')
        self.assertEquals(resolve(url).func.view_class, GlobalStatView)
