from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required
def homepage(request):
    """Metodo che reindirizza l'Homepage
    :param request: richiesta http inviata dall'utente al server
    :return: Il render della homepage."""
    return render(request, 'home.html')

@login_required
def removeAccount(request):
    """Metodo che riceve la richiesta di rimozione  dell'account
    da parte dell'utente e la esegue.
    :param request: richiesta http inviata dall'utente al server
    :return: Il render della pagina di login."""
    user = User.objects.get(username=request.user)
    #print(user.username)
    user.delete()
    return render(request, 'registration/login.html')

