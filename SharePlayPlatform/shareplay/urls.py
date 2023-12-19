# shareplay/urls.py

from django.urls import path
from .views import Games, Users, Transactions

urlpatterns = [
    path('games/', Games.as_view(), name='Games'),
    path('users/', Users.as_view(), name='Users'),
    path('transactions/', Transactions.as_view(), name='Transactions'),
    
]
