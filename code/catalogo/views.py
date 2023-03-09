from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from accounts.models import Blacklist
from catalogo.forms import TextCrispyFormComplete, TranslateForm
from catalogo.models import Testo, Token
from synonyms.synonyms import Synonyms

from .filters import TextFilter
from translation.translate import Translate
from accounts.current_user import get_current_user


@method_decorator(login_required, name='dispatch')
class TextAdd(CreateView):
    """Vista utilizzata per creare la pagina dove l'untente loggato può inserire un testo.
    La classe riceve in input le informazioni inserite dall'utente attraverso il form di inserimento del testo.
    Inoltre controlla che i campi siano stati correttamente compilati."""

    model = Testo
    template_name = 'catalogo/insertText.html'

    form_class = TextCrispyFormComplete

    def get_success_url(self):
        """Mostra un messaggio di errore nel caso in cui uno o più campi non siano stati correttamente compilati e
        reindirizza alla pagina corretta in base a quanto richesto dall'utente nel form.
        :return: Reindirizza alla pagina di inserimento del testo nel caso la checkanalyze 'Visualizza risultati'
        non sia abilitata. Altrimenti reindirizza alla pagina di visualizzazione dell'analisi del testo."""

        if not Testo.success:
            messages.error(self.request, 'Uno dei campi inseriti non è valido')
            return reverse_lazy('catalogo:insert-text')
        else:
            return reverse_lazy('catalogo:visualizza-text', kwargs={'pk': Testo.objects.last().id})


@method_decorator(login_required, name='dispatch')
class TextView(ListView):
    """Vista utilizzata per creare la pagina dove l'untente loggato può visualizzare l'analisi di un testo
    che ha selezionato/inserito."""
    form_class = TranslateForm
    model = Token
    template_name = 'catalogo/visualizza_risultati.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Metodo che seleziona il testo di cui bisogna visualizzare le informazioni e i relativi token.
        :return: Riferimenti al testo e i relativi token corretti da visualizzare."""
        if 'form' not in kwargs:
            kwargs['form'] = self.form_class
            context = super().get_context_data(**kwargs)
            context['text'] = Testo.objects.filter(id=self.kwargs['pk']).values()
            context['token'] = Token.objects.filter(testo_id=self.kwargs['pk']).values().order_by('-frequenza')
            '''Recupero del data-set per la creazione del grafico'''
            frequency_dict = {}

            for ft in context['token']:
                if frequency_dict.get(ft.get('frequenza')) is None:
                    frequency_dict[ft.get('frequenza')] = 1
                else:
                    frequency_dict[ft.get('frequenza')] += 1

            frequency = [x for x in frequency_dict.keys()]
            occurency = [x for x in frequency_dict.values()]

            notFilteredTokens = Token.objects.filter(testo_id=self.kwargs['pk']).values('parola')
            blacklistObj = Blacklist.objects.filter(utente=get_current_user()).values("parola")
            token = notFilteredTokens.difference(blacklistObj)
            dati = []
            for t in token:
                '''Recupero la frequenza della parola nel primo testo, se essa non è presente imposto la frequenza a 
                zero '''
                freq_t = Token.objects.filter(testo_id=self.kwargs['pk'], parola=t["parola"]).values(
                    "frequenza").first()
                dati.append({'parola': t['parola'], 'frequenza': freq_t.get('frequenza')})
            dati.sort(key=lambda x: x['frequenza'], reverse=True)
            context['token'] = dati
            context['frequency'] = frequency[::-1]
            context['occurency'] = occurency[::-1]

        if self.request.GET.get('lang') is not None:
            tokens = [t['parola'] for t in context['token']]
            try:
                T = Translate(tokens, self.request.GET.get('lang'))
                context['trad'] = T.get_translated_words()
            except:
                context['trad'] = "err"

        if 'sinonimi' in self.request.GET.keys():
            tokens = [t['parola'] for t in context['token']]
            synonyms = Synonyms(tokens)

            context['first_synonyms'] = []
            for t in synonyms.getSynonyms():
                dictionary = {}
                for key, j in t.items():
                    count = 0
                    for element in j:
                        if key != 'parola' and count < 2:
                            if count == 0:
                                dictionary[str(key)] = []
                            dictionary[str(key)].append(element)
                            count += 1
                if not dictionary:
                    dictionary['null'] = 'True'
                context['first_synonyms'].append(dictionary)

        return context


@login_required
def TextSearchCompare(request):
    """Metodo che renderizza alla pagina di ricerca per due testi da comparare. Inoltre mostra i risultati della query effettuata dall'utente.
    :return: Il render della pagina di ricerca."""
    text_list = Testo.objects.all()
    text_filter = TextFilter(request.GET, queryset=text_list)

    previous_url = str(request.META.get('HTTP_REFERER'))
    if 'compare' not in previous_url:
        return render(request, 'catalogo/searchCompareText.html', {'filter': text_filter, 'clean': True}, )
    else:
        return render(request, 'catalogo/searchCompareText.html', {'filter': text_filter, 'clean': False}, )


@method_decorator(login_required, name='dispatch')
class ViewCompare(ListView):
    model = Token
    template_name = 'catalogo/text-compare.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['text1'] = Testo.objects.filter(id=self.kwargs['pk1']).values()
        context['user1'] = User.objects.filter(id=context['text1'][0].get('pubblicatore_id')).values('username')

        context['text2'] = Testo.objects.filter(id=self.kwargs['pk2']).values()
        context['user2'] = User.objects.filter(id=context['text2'][0].get('pubblicatore_id')).values('username')

        token1 = Token.objects.filter(testo_id=self.kwargs['pk1']).values("parola")
        token2 = Token.objects.filter(testo_id=self.kwargs['pk2']).values("parola")

        dati = {}

        notFilteredTokens = token1.union(token2)
        blacklistObj = Blacklist.objects.filter(utente=get_current_user()).values("parola")
        token = notFilteredTokens.difference(blacklistObj)

        for t in token:
            '''Recupero la frequenza della parola nel primo testo, se essa non è presente imposto la frequenza a zero'''
            freq_t1 = Token.objects.filter(testo_id=self.kwargs['pk1'], parola=t["parola"]).values("frequenza").first()
            if freq_t1 is None:
                freq_t1 = {'frequenza': 0}

            '''Recupero la frequenza della parola nel secondo testo, se essa non è presente imposto la frequenza a 
            zero '''
            freq_t2 = Token.objects.filter(testo_id=self.kwargs['pk2'], parola=t["parola"]).values("frequenza").first()
            if freq_t2 is None:
                freq_t2 = {'frequenza': 0}

            '''Imposto un dizionario {'parola':[freqenza_testo1, freqenza_testo2]} per passarlo successivamente come 
            contesto '''
            dati[t["parola"]] = [freq_t1.get('frequenza'), freq_t2.get('frequenza')]

        context['data'] = dati

        return context


@login_required
def search(request):
    """Metodo che renderizza la pagina di ricerca. Inoltre mostra i risultati della query effettuata dall'utente.
    :return: Il render della pagina di ricerca."""
    text_list = Testo.objects.all()
    text_filter = TextFilter(request.GET, queryset=text_list)
    return render(request, 'catalogo/searchText.html', {'filter': text_filter})


@method_decorator(login_required, name='dispatch')
class GlobalStatView(ListView):
    """Vista utilizzata per creare la pagina dove l'untente loggato può visualizzare l'analisi di un testo
    che ha selezionato/inserito."""
    model = Token
    template_name = 'catalogo/globalStatistic.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        text_list = Testo.objects.all()
        context = super().get_context_data(**kwargs)

        if len(text_list) == 0:
            context['empty'] = 1
        else:
            context['empty'] = 0
            average_IC = average_Text_Length = average_lexical_density = 0
            # calcolo dei punteggi medi
            for rec in text_list:
                average_IC += rec.complessita
                average_Text_Length += rec.term_totali
                average_lexical_density += (rec.term_unici / rec.term_totali)

            average_IC /= len(text_list)
            average_Text_Length /= len(text_list)
            average_lexical_density /= len(text_list)

            context['averageIC'] = round(average_IC, 1)
            context['averageTL'] = int(average_Text_Length)
            context['averageLD'] = round(average_lexical_density, 3)

            # calcolo delle frequenze complessive
            token_list = Token.objects.all()

            tokens = {}
            for k in token_list:
                if k.parola not in tokens.keys():
                    tokens[k.parola] = k.frequenza
                else:
                    tokens[k.parola] += k.frequenza

            blacklistObj = Blacklist.objects.filter(utente=get_current_user()).values("parola")
            blacklistTokens = [blacklistObj[i]['parola'] for i in range(len(blacklistObj))]
            for t in blacklistTokens:
                if t in tokens:
                    tokens.pop(t)
            context['token_dict'] = {k: v for k, v in sorted(tokens.items(), key=lambda x: x[1], reverse=True)}
        return context
