# shareplay/urls.py

from django.urls import path
from .views import isFav, Games,addComment,getAvatar, Users, Transactions, Gameslist,ReviewCreate, Userslist, Transactionslist  ,GamesDetail, profile, updateProfile, add, ReviewsDetails
urlpatterns = [
    path('games/', Games.as_view(), name='Games'),
    path('users/', Users.as_view(), name='Users'),
    path('getProfile/<username>/', profile, name='Users'),
    path('invoice/', Transactions.as_view(), name='Transactions'),
    path('gameslist/', Gameslist.as_view(), name='Gameslist'),
    path('userslist/', Userslist.as_view(), name='Userslist'),
    path('invoicelist/', Transactionslist.as_view(), name='Transactionslist'),
    path('review/<game_slug>/', ReviewCreate.as_view(), name='ReviewCreate'),
    path('gamesdetail/<slug>/', GamesDetail.as_view(), name='GamesDetail'),
    path('updateProfile/',updateProfile, name='updateProfile'),
    path('getComments/<game_slug>/', ReviewsDetails.as_view(), name='GamesDetail'),
    path('isFav/<slug>',isFav, name='add'),
    path('add',add, name='add'),
    path('addComment/<game_slug>',addComment, name='add'),
    path('getAvatar/<id>',getAvatar, name='add'),
    
    
]
