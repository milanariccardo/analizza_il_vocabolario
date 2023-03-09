from django.contrib.auth.models import User
from django.db import models

from accounts.current_user import get_current_user


class Testo(models.Model):
    """Classe che descrive la tabella Testo, con campi: titolo, autore, tipo, descrizione,
    pubblicatore, termini unici, termini totali, complessità."""

    scelta_tipo = (
        ('1', 'Tema scolastico'),
        ('2', 'Saggio'),
        ('3', 'Articolo di giornale'),
        ('4', 'Altro'),
    )

    # Chiave primaria "id" assegnata in automatico da Django
    titolo = models.CharField(max_length=255)
    autore = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=30, choices=scelta_tipo, default='1')
    descrizione = models.CharField(max_length=300, blank=True)
    term_unici = models.IntegerField(default=0)
    term_totali = models.IntegerField(default=0)
    complessita = models.IntegerField(default=0)
    pubblicatore = models.ForeignKey('auth.User', default=get_current_user, on_delete=models.CASCADE, )
    text_complete = ""

    combo_filter = None
    success = False
    T = None

    # La classe viene visualizzata con il titolo
    def __str__(self):
        """Metodo che ridefinisce il modo in cui un record della tabella Testo viene stampato."""
        return f'id: {self.id} - Titolo: {self.titolo} '

    def save(self, *args, **kwargs):
        """Metodo che salva i testi e i token relativi ad esso nel database."""
        if not self.success:
            return
        self.term_totali = self.T.getTotalNumberOfTerms()
        self.term_unici = self.T.getCardinality()
        self.complessita = self.T.getComplexityIndex()

        super().save(*args, **kwargs)

        for t, f in self.T.getVocabulary().items():
            token = Token()
            token.testo = self
            token.parola = t
            token.frequenza = f
            token.save()

    # Nome plurale
    class Meta:
        verbose_name_plural = 'Testi'


class Token(models.Model):
    """Classe che descrive la tabella Token, con campi: testo, parola, frequenza."""

    class Meta:
        unique_together = (('testo', 'parola'),)

    testo = models.ForeignKey(Testo, on_delete=models.CASCADE)
    parola = models.CharField(max_length=30)
    frequenza = models.IntegerField(default=0)

    def __str__(self):
        """Metodo che ridefinisce il modo in cui un record della tabella Token viene stampato."""
        return f'testo: {self.testo} - parola: {self.parola} '
