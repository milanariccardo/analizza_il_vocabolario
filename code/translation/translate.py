from googletrans import Translator


class Translate:
    """Classe utile al calcolo della traduzione delle parole di una lista ricevuta in ingresso.
    :param word: Iterabile lista contente le parole da tradurre.
    :param lang: La lingua in cui le parole devono essere tradotte"""
    def __init__(self, word, lang):
        self.translatedWords = []
        self.translator = Translator()
        self.text = ""
        self.textTranslated = ""
        self.translation(word, lang)

    def translation(self, word, lang):
        """Funzione che calcola la traduzione delle parole passate come argomento nella lingua selezionata
        :param word: Lista di parole da tradurre
        :param lang: Lingua di destinazione"""
        for w in word:
            self.text += w + "\n"
        self.textTranslated = self.translator.translate(self.text, src='it', dest=lang).text
        self.textTranslated = self.textTranslated.replace(' ', '-')
        self.textTranslated = self.textTranslated.replace('\n', ' ')
        self.textTranslated = self.textTranslated.split(" ")

        for w in self.textTranslated:
            if '-' in w:
                w = w.replace('-', ' ')
            self.translatedWords.append(w.lower())
        self.translatedWords.reverse()

    def get_translated_words(self):
        """Ritorna un dizionario contente le parole tradotte"""
        return self.translatedWords
