
from rest_framework import generics
from .models import Game, UserProfile, Transaction
from .serializers import GameSerializer, UserSerializer, TransactionSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User as AuthUser

class Games(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class Users(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class Transactions(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class Gameslist(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class Userslist(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class Transactionslist(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class GamesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'slug'


def profile(request,username):
    if request.user.is_authenticated and request.user.username == username:
       email=request.user.email
    else:
       email=""
    user=AuthUser.objects.get(username=username)
    user=UserProfile.objects.get(user=user)
    return JsonResponse({'username': user.user.username, 'email': email,
                         'nickname': user.nickname, 'avatar': user.avatar.url,
                         'bio': user.bio,
                         'header': user.header.url,})
