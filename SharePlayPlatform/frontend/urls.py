from django.urls import path

from .views import index , detail, login, register, search,Profile

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('profile', Profile),
    path('search',search),
    path('game/<slug:slug>/', detail),
    path('login/', login),
    path('register/', register),
]