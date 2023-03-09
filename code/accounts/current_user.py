from threading import local
from django.utils.deprecation import MiddlewareMixin

_user = local()


class CurrentUserMiddleware(MiddlewareMixin):
    """Classe che ci permette di recuperare l'username dell'utente loggato"""

    def process_request(self, request):
        """Metodo che recupera, partendo da un oggetto request, l'username
        dell'utente loggato
        :param:richiesta
        """
        _user.request = request

    def process_response(self, request, response):
        """Metodo che processa la risposta prima di restituirla al browser
        :return:risposta processata"""
        if hasattr(_user, 'request'):
            del _user.request
        return response


def get_current_request():
    """Ritorna la richiesta per il thread corrente
    :return:richiesta thread corrente"""
    return getattr(_user, "request", None)


def get_current_user():
    """Metodo get che restituisce l'username dell'utente loggato senza passare l'oggetto request
    :return:username utente loggato"""
    request = get_current_request()
    if request:
        return getattr(request, "user", None)
