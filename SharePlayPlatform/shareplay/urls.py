# shareplay/urls.py

from django.urls import path
from .views import Games, Users, Transactions, Gameslist, Userslist, Transactionslist , GamesDetail, profile, updateProfile

urlpatterns = [
    path('games/', Games.as_view(), name='Games'),
    path('users/', Users.as_view(), name='Users'),
    path('getProfile/<username>/', profile, name='Users'),
    path('invoice/', Transactions.as_view(), name='Transactions'),
    path('gameslist/', Gameslist.as_view(), name='Gameslist'),
    path('userslist/', Userslist.as_view(), name='Userslist'),
    path('invoicelist/', Transactionslist.as_view(), name='Transactionslist'),
    path('gamesdetail/<slug>/', GamesDetail.as_view(), name='GamesDetail'),
    path('updateProfile/',updateProfile, name='updateProfile')
    
    
]
