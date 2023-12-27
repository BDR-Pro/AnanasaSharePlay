from django.urls import path

from .views import index , detail, login, register, search,Profile,MyGames,genre,pay,renting,RentYourGame,rents,check_invoice_payment_status

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('rent-your-game/<id>',RentYourGame),
    path('profile', Profile),
    path('Profile/rents', rents, name='profile'),
    path('MyGames',MyGames),
    path('search',search),
    path('game/<slug:slug>/', detail, name='game_detail'),
    path('game/<slug:slug>/listing/', renting),
    path('game/genre/<slug>/', genre, name='genre'),
    path('login/', login),
    path('register/', register),
    path('pay/<randomNumber>',pay,name='pay'),
    path('Profile',Profile),
    path('NewInvoice',check_invoice_payment_status,name='NewInvoice')
]