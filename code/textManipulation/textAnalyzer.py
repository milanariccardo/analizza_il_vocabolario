# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:16:33 2020
@author: Andrea Canaris & Andrea Ianniciello
"""


class TextAnalyzer:
    """Classe utilizzata per effettuare la manipolazione del testo inserito.
    Inizializzando la classe con un testo, questo viene automaticamente scomposto
    in token e ne viene calcolata la frequenza. Si rimuovono inoltre i segni di interpunzione.
    Vengono anche calcolate alcune statistiche relative al testo.
    :param text: testo da analizzare
    :param filt: filtro sulle lettere di una certa lunghezza"""

    def __init__(self, text, filt=None):
        self.totalNumberOfWords = 0
        self.numberOfLettersFilter = filt
        self.vocabulary = self.tokenizer(text)
        self.numberOfVocabularyWords = len(self.vocabulary)                      # !!!!!!!!!!!!!!!
        self.lexicalDensity = self.setLexicalDensity()
        self.complexityIndex = self.textComplexity()

    def tokenizer(self, text):
        """Metodo che converte il testo in lowercase e lo scompone in token,
        rimuovendone anche i segni di interpunzione. Calcola infine la
        frequenza dei termini."""
        from nltk.tokenize import RegexpTokenizer
        '''di sotto la funzione da usare per estrarre le frasi dal testo'''
        tokReg = RegexpTokenizer(r'\w+')
        tokens = tokReg.tokenize(text.lower())
        if self.getFilter() is not None:
            lis = [i for i in tokens if len(i) <= int(self.getFilter())]
            for j in lis:
                tokens.remove(j)
        assert len(tokens) > 0
        self.totalNumberOfWords = len(tokens)

        T = {}
        for t in tokens:
            if t not in T:
                T[t] = 1
            else:
                T[t] += 1
        return T

    def textComplexity(self):
        """Funzione che calcola la complessità di un testo. Massima complessità 1000"""
        import syllables
        somma = sum([syllables.estimate(t) / v for t, v in self.vocabulary.items()])
        return (somma * self.lexicalDensity) / 10

    def getTotalNumberOfTerms(self):
        """Ritorna il numero delle parole totali del testo."""
        return self.totalNumberOfWords

    def getCardinality(self):
        """Ritorna la cardinalità del vocabolario del testo inserito"""
        return self.numberOfVocabularyWords

    def getLexicalDensity(self):
        """Ritorna la densità lessicale del testo."""
        return self.lexicalDensity

    def getComplexityIndex(self):
        """Ritorna l'indice di complessità."""
        return self.complexityIndex

    def getVocabulary(self):
        """Ritorna il vocabolario del testo, comprendente coppie del tipo
            Termine:Frequenza."""
        return self.vocabulary

    def setLexicalDensity(self):
        return self.numberOfVocabularyWords / self.totalNumberOfWords

    def getFilter(self):
        return self.numberOfLettersFilter
