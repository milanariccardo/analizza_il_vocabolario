from django.contrib import admin
from django.urls import path, include
from catalogo import views
from django.views.generic import TemplateView

app_name = 'catalogo'
urlpatterns = [
    path('insert/', views.TextAdd.as_view(), name='insert-text'),
    path('visualizza/<int:pk>', views.TextView.as_view(), name='visualizza-text'),
    path('search/', views.search, name='search'),
    path('compare/', views.TextSearchCompare, name='text-search-compare'),
    path('compare/view/<int:pk1>-<int:pk2>', views.ViewCompare.as_view(), name='text-compare'),
    path('statistiche-globali/', views.GlobalStatView.as_view(), name='statistiche_globali'),
]