
from rest_framework import generics
from .models import Game, User, Transaction
from .serializers import GameSerializer, UserSerializer, TransactionSerializer

class Games(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class Users(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Transactions(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


