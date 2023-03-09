from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('blacklist/', views.BlacklistView.as_view(), name='blacklist'),
    path('delete-word/<int:pk>', views.DeleteBlacklistWord.as_view(), name="delete_word")
]