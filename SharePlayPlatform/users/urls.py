from django.urls import path
from .views import login_view, register_view, logout_view, is_user_authenticated, profile
urlpatterns = [
    path('',is_user_authenticated, name='is_user_authenticated'),
    path('<username>',profile, name='profile_view'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
]
