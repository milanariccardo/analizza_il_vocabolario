from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, DeleteView

from accounts.current_user import get_current_user
from accounts.forms import BlacklistForm
from accounts.models import Blacklist


class SignUp(generic.CreateView):
    """Vista utilizzata per creare la pagina in cui un nuovo utente,
    può iscriversi. La classe riceve in input le informazioni inserite dall'utente
    attraverso il form di registrazione."""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@method_decorator(login_required, name='dispatch')
class BlacklistView(CreateView):
    form_class = BlacklistForm
    model = Blacklist
    template_name = 'accounts/blacklist.html'

    def get_success_url(self):
        """Mostra un messaggio di errore nel caso in cui uno o più campi non siano stati correttamente compilati e
        reindirizza alla pagina corretta in base a quanto richesto dall'utente nel form.
        :return: Reindirizza alla pagina di inserimento del testo nel caso la checkanalyze 'Visualizza risultati'
        non sia abilitata. Altrimenti reindirizza alla pagina di visualizzazione dell'analisi del testo."""
        if not Blacklist.success:
            messages.error(self.request, 'Inserire una parola valida')
        else:
            if not Blacklist.repeated:
                messages.success(self.request, 'Parole inserite nella blacklist')
            else:
                messages.error(self.request,
                               'Una o più parole non sono state inserite perchè già presenti nella blacklist')
        return reverse_lazy('blacklist')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['blacklist'] = Blacklist.objects.filter(utente=get_current_user()).values('parola')
        return context


@method_decorator(login_required, name='dispatch')
class DeleteBlacklistWord(DeleteView):
    model = Blacklist
    success_url = reverse_lazy('blacklist')