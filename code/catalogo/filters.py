from django.contrib.auth.models import User
import django_filters

from catalogo.models import Testo


class TextFilter(django_filters.FilterSet):
    """Classe che implementa un filtro per i model."""

    titolo = django_filters.CharFilter(lookup_expr='icontains')
    autore = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Testo
        fields = ['titolo', 'autore', 'tipo', 'pubblicatore']
