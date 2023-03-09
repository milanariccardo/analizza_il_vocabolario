from nltk.corpus import wordnet as wn


class Synonyms:
    """Classe che trova i sinonimi per ogni parola passata come argomento
    :param words: Lista di parole"""
    def __init__(self, words):
        self.synonyms = [self.findSynonyms(t) for t in words]

    @staticmethod
    def findSynonyms(term):
        """Metodo che trova i sinonimi e li suddivide per categorie
        :param term: Parola"""
        synonyms = {'Aggettivo': [], 'Nome': [], 'Avverbio': [], 'Verbo': [], 'parola': term}
        categorie = {'a': 'Aggettivo', 'n': 'Nome', 'r': 'Avverbio', 'v': 'Verbo', 's': 'Aggettivo'}
        for synset in wn.synsets(term, lang='ita'):
            for lemma in synset.lemmas(lang='ita'):
                word = lemma.name()
                if '_' in word:
                    word = word.replace('_', ' ')
                synonyms[categorie[synset.pos()]].append(word)

        # Ciclo che rimuove i termini duplicati presenti nella lista dei sinonimi
        for k in synonyms.keys():
            if k != 'parola':
                synonyms[k] = list(dict.fromkeys(synonyms[k]))
                try:
                    synonyms[k].remove(term)
                except:
                    pass
        return synonyms

    def getSynonyms(self):
        """Funzione che ritorna la lista dei sinonimi
        :return: Lista dei sinonimi"""
        self.synonyms.reverse()
        return self.synonyms
