from django.urls import path

from .views import index , detail, login, register, search,Profile

urlpatterns = [
    path('', index),
    path('Profile', Profile),
    path('search',search),
    path('game/<slug:slug>/', detail),
    path('login/', login),
    path('register/', register),
]