from django.test import TestCase

from synonyms.synonyms import Synonyms


class TestModels(TestCase):
    """Classe utilizzata per testare i sinonimi"""

    @staticmethod
    def findTerm(term, listTerm):
        return term in listTerm

    def testEmptyList(self):
        """Metodo che prende in ingresso una lista vuota e non deve ritornare alcun sinonimo"""
        listEmpty = []
        synonymsTest = Synonyms(listEmpty)
        self.assertEqual([], synonymsTest.getSynonyms())

    def testNotExistingWord(self):
        """Metodo che prende in ingresso una parola inesistente e non ritorna alcun sinonimo"""
        listWrongWord = ['opdodo']
        synonymsTest = Synonyms(listWrongWord)
        dictAspected = {'Aggettivo': [], 'Nome': [], 'Avverbio': [], 'Verbo': [], 'parola': 'opdodo'}
        self.assertEqual([dictAspected], synonymsTest.getSynonyms())

    def testPunctuation(self):
        """Metodo che prende in ingresso punteggiature e non ritorna alcun sinonimo"""
        listWrongWord = ['..,.']
        synonymsTest = Synonyms(listWrongWord)
        dictAspected = {'Aggettivo': [], 'Nome': [], 'Avverbio': [], 'Verbo': [], 'parola': '..,.'}
        self.assertEqual([dictAspected], synonymsTest.getSynonyms())

    def testOnlyNumber(self):
        """Metodo che prende in ingresso una parola inesistente e non ritorna alcun sinonimo"""
        listWrongWord = ['12345']
        synonymsTest = Synonyms(listWrongWord)
        dictAspected = {'Aggettivo': [], 'Nome': [], 'Avverbio': [], 'Verbo': [], 'parola': '12345'}
        self.assertEqual([dictAspected], synonymsTest.getSynonyms())

    def testCorrectWord(self):
        """Metodo che prende in ingresso una parola valida che ha dei sinonimi e ritorna i suoi sinonimi"""
        """ Prende come parola 'prova' e cerca se tra i sinonimi restituiti è presente almeno 'test' """
        listWord = ['prova']
        synonymsTest = Synonyms(listWord)
        self.assertEqual(True, self.findTerm('test', synonymsTest.getSynonyms()[0].get('Nome')))

    def testDoubleMeaningWord(self):
        """Metodo che prende in ingresso una parola con più significati e dovrebbe ritornare i sinonimi di entrambi i
        significati. Nel nostro caso ci aspettiamo che fallisca, in quanto abbiamo un debito tecnico riguardo parole con
        più significati"""
        listWord = ['botte']
        synonymsTest = Synonyms(listWord)
        self.assertEqual(True, self.findTerm('barile', synonymsTest.getSynonyms()[0].get('Nome')))
        self.assertEqual(False, self.findTerm('picchiare', synonymsTest.getSynonyms()[0].get('Verbo')))
