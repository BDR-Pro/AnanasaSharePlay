from django.urls import path

from .views import index , detail, login, register, search,Profile,MyGames,genre,renting,RentYourGame

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('rent-your-game/<id>',RentYourGame),
    path('profile', Profile),
    path('MyGames',MyGames),
    path('search',search),
    path('game/<slug:slug>/', detail),
    path('game/<slug:slug>/listing/', renting),
    path('game/genre/<slug>/', genre),
    path('login/', login),
    path('register/', register),
]