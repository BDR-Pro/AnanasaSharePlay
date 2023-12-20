from django.urls import path

from .views import index , detail, login, register

urlpatterns = [
    path('', index),
    path('game/<slug:slug>/', detail),
    path('login/', login),
    path('register/', register),
]