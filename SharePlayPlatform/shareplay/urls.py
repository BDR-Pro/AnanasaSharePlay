# shareplay/urls.py

from django.urls import path
from .views import getGames, getUsers, getTransactions, addGame, removeGame , addUser , removeUser , initiateTransaction

urlpatterns = [
    path('games/', getGames, name='get_games'),
    path('users/', getUsers, name='get_users'),
    path('transactions/', getTransactions, name='get_transactions'),
    path('addGame', addGame, name='add_game'),
    path('removeGame/<int:game_id>', removeGame, name='remove_game'),
    path('addUser', addUser, name='add_user'),
    path('removeUser/<int:user_id>', removeUser, name='remove_user'),
    path('newInovice', initiateTransaction, name='initiate_transaction')
]
