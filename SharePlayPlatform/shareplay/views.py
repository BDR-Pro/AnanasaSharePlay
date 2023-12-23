
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


def updateProfile(request):
    if request.user.is_authenticated and request.method == 'POST' :
        user=AuthUser.objects.get(username=request.user.username)
        user=UserProfile.objects.get(user=user)
        if request.POST.get('password'):
            user.user.set_password(request.POST.get('password'))
        if request.POST.get('username'):
            user.user.username=request.POST.get('username') if not AuthUser.objects.filter(username=request.POST.get('username')).exists() else user.user.username
        user.user.email=request.POST.get('email') if request.POST.get('email') else user.user.email
        user.nickname=request.POST.get('nickname') if request.POST.get('nickname') else user.nickname
        user.bio=request.POST.get('bio') if request.POST.get('bio') else user.bio
        user.avatar=request.FILES.get('avatar') if request.FILES.get('avatar') else user.avatar
        user.header=request.FILES.get('header') if request.FILES.get('header') else user.header
        user.save()
        return JsonResponse({'username': user.user.username, 'email': user.user.email,
                         'nickname': user.nickname, 'avatar': user.avatar.url,
                         'bio': user.bio,
                         'header': user.header.url,})
    else:
        return JsonResponse({'username': "", 'email': "",
                         'nickname': "", 'avatar': "",
                         'bio': "",
                         'header': "",})
        
        
        



def add(request):
    if request.user.is_authenticated and request.method == 'POST' :
        game=Game.objects.get(slug=request.POST.get('id'))
        user=AuthUser.objects.get(username=request.user.username)
        user=UserProfile.objects.get(user=user)
        if not Transaction.objects.filter(game=game,user=user).exists():
            transaction=Transaction(game=game,user=user)
            transaction.save()
            return JsonResponse({'status': "success"})
        else:
            return JsonResponse({'status': "fail"})
    else:
        return JsonResponse({'status': "Use POST method"})