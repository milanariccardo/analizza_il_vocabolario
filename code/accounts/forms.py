from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from textManipulation.textAnalyzer import TextAnalyzer
from accounts.models import Blacklist


class BlacklistForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'language-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Inserisci'))

    class Meta:
        model = Blacklist
        fields = 'parola',

    def save(self, commit=True):
        """Metodo che controlla che i dati inseriti siano corretti, nel caso procede con il salvataggio.
        Blocca il processo altrimenti."""

        # Controllo sulla parola
        parola_blacklist = self.cleaned_data.get('parola', None)

        try:
            Blacklist.T = TextAnalyzer(parola_blacklist)
            Blacklist.success = True
        except AssertionError:
            Blacklist.success = False

        return super().save(commit)
