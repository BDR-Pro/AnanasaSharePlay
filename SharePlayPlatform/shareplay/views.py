from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, User, Transaction
from .serializers import GameSerializer, UserSerializer, TransactionSerializer

@api_view(['GET'])
def getGames(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTransactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addGame(request):
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        game = serializer.save()
        return Response(GameSerializer(game).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def removeGame(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        game.delete()
        return Response({"message": "Game deleted successfully"}, status=204)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=404)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def removeUser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=204)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['POST'])
def initiateTransaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        transaction = serializer.save()
        return Response(TransactionSerializer(transaction).data, status=201)
    return Response(serializer.errors, status=400)
