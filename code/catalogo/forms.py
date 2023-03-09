from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from textManipulation.textAnalyzer import TextAnalyzer

from catalogo.models import Testo
from googletrans import LANGUAGES


def getLanguages():
    """metodo che ritorna la lista delle lingue disponibili"""
    lang_choices = [(lang, LANGUAGES[lang]) for lang in LANGUAGES]
    return tuple(lang_choices)


languageChoices = getLanguages()


class TranslateForm(forms.Form):
    """Classe che implementa il campo scelta della lingua nel template visualizza_risultati.html"""
    lang = forms.ChoiceField(choices=languageChoices, label="Lingua", initial="en")


class TextCrispyForm(forms.ModelForm):
    """Classe che definisce l'implementazione del form per l'inserimento del testo."""

    helper = FormHelper()
    helper.form_id = 'language-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Inserisci'))

    class Meta:
        model = Testo
        fields = ('titolo', 'autore', 'tipo', 'descrizione')


class TextCrispyFormComplete(TextCrispyForm):
    """Classe che aggiunge due campi (text_complete, check_analyze) al TextCrispyForm,
    non compresi nel model Testo."""

    filterChoices = (
        (None, 'Nessun filtro'),
        (1, '1 carattere'),
        (2, '2 caratteri'),
    )

    text_complete = forms.CharField(widget=forms.Textarea(), required=True, label="Inserisci il testo")
    combo_filter = forms.ChoiceField(choices=filterChoices, required=False,
                                     label="Filtra le parole con un numero di caratteri minori di:")

    def save(self, commit=True):
        """Metodo che controlla che i dati inseriti siano corretti, nel caso procede con il salvataggio.
        Blocca il processo altrimenti."""
        Testo.text_complete = self.cleaned_data.get('text_complete', None)
        Testo.combo_filter = self.cleaned_data.get('combo_filter', None)

        if Testo.combo_filter == "":
            Testo.combo_filter = None

        # Controllo su Titolo, Autore
        titolo = self.cleaned_data.get('titolo', None)
        autore = self.cleaned_data.get('autore', None)

        try:
            if autore != "":
                Testo.T = TextAnalyzer(autore)
            Testo.T = TextAnalyzer(titolo)
            Testo.T = TextAnalyzer(Testo.text_complete, Testo.combo_filter)
            Testo.success = True
        except AssertionError:
            Testo.success = False

        return super().save(commit)

    class Meta(TextCrispyForm.Meta):
        fields = TextCrispyForm.Meta.fields + ('text_complete', 'combo_filter',)
