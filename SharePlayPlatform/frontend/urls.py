from django.urls import path

from .views import index , detail, login, register, search,Profile,MyGames,genre

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('profile', Profile),
    path('MyGames',MyGames),
    path('search',search),
    path('game/<slug:slug>/', detail),
    path('game/genre/<slug>/', genre),
    path('login/', login),
    path('register/', register),
]