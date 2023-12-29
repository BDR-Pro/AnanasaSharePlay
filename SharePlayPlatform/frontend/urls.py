from django.urls import path

from .views import index ,Statistic,play,listed, detail, login, DeleteYourGame ,register, search,Profile,MyGames,genre,pay,renting,RentYourGame,rents,check_invoice_payment_status,RateStreamer

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('Statistic',Statistic,name='Statistic'),
    path('rent-your-game/<id>',RentYourGame),
    path('delete-your-game/<id>', DeleteYourGame),
    path('profile', Profile),
    path('Profile/rents', rents, name='profile'),
    path('Profile/listed/<username>',listed,name='listed'),
    path('MyGames',MyGames),
    path('search',search),
    path('game/<slug:slug>/', detail, name='game_detail'),
    path('game/<slug:slug>/listing/', renting),
    path('game/genre/<slug>/', genre, name='genre'),
    path('login/', login),
    path('register/', register),
    path('pay/<randomNumber>',pay,name='pay'),
    path('Profile',Profile),
    path('NewInvoice',check_invoice_payment_status,name='NewInvoice'),
    path('RateStreamer/<Transid>',RateStreamer,name='RateStreamer'),
    path('play/<Transid>/', play, name='play')
]