
from rest_framework import generics
from .models import Game, UserProfile, Transaction
from .serializers import GameSerializer, UserSerializer, TransactionSerializer

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
