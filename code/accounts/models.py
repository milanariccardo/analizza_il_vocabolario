from django.db import models

from accounts.current_user import get_current_user


class Blacklist(models.Model):
    """Classe che descrive la tabella Blacklist, con campi: utente e parola."""
    class Meta:
        unique_together = (('utente', 'parola'),)

    utente = models.ForeignKey('auth.User', default=get_current_user, on_delete=models.CASCADE)
    parola = models.CharField(max_length=255)
    success = False  # se l'utente inserisce una parola non valida
    repeated = False  # se l'utente inserisce parole già presenti nella blacklist
    T = None

    def save(self, *args, **kwargs):
        """Metodo che salva le blackword nel database."""
        if not self.success:
            return

        Blacklist.repeated = False
        self.parola = [k for k in self.T.getVocabulary().keys()]
        db = Blacklist.objects.values_list('parola').filter(utente=self.utente)
        # prendiamo le parole già inserite nella blacklist
        blacklistWords = [w[0] for w in db]

        obj = []
        for w in self.parola:
            if not blacklistWords:
                obj.append(Blacklist(parola=w, utente=self.utente))
            else:
                if w not in blacklistWords:
                    obj.append(Blacklist(parola=w, utente=self.utente))
                else:
                    Blacklist.repeated = True
        Blacklist.objects.bulk_create(obj)
