
from rest_framework import generics
from .models import Game, UserProfile, Transaction, Reviews,RateStreamerModel,Listing
from datetime import datetime, timezone
from django.db.models import Sum, F, ExpressionWrapper, fields
from .serializers import GameSerializer, UserSerializer, TransactionSerializer, ReviewsSerializer
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.models import User as AuthUser
import json
from django.shortcuts import get_object_or_404

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
    

class ReviewsDetails(generics.ListAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        game_slug = self.kwargs['game_slug']
        return Reviews.objects.filter(game__slug=game_slug)
    


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        game_slug = self.kwargs['game_slug']
        return Reviews.objects.filter(game__slug=game_slug)




def profile(request,username):
    if request.user.is_authenticated and request.user.username == username:
       email=request.user.email
    else:
       email=""
    user=AuthUser.objects.get(username=username)
    playedGames=Transaction.objects.filter(user=user,isPlayed=True).count()
    NumberOfListedGames=Listing.objects.filter(user=user).count()
    revenue = Transaction.objects.filter(user=user, is_paid=True).aggregate(
        total_revenue=Sum('revenue')
    )['total_revenue']

    print(revenue)
    revenue = revenue if revenue else 0
    recentlyPlayedGames=Transaction.objects.filter(rented_user=user,isPlayed=True).order_by('-start_date','-start_hour')[:5]
    print(recentlyPlayedGames)
    today = datetime.now(timezone.utc).date()
    mylistedGames=Listing.objects.filter(end__gt=today,user=user).order_by('-starting_time')[:3]
    mylistedGames=list(mylistedGames.values())
     
    for game in mylistedGames:
        avatar = Game.objects.get(id=game['game_id']).image.url
        title = Game.objects.get(id=game['game_id']).title
        slug = Game.objects.get(id=game['game_id']).slug
        game['game_avatar'] = avatar
        game['game_title'] = title
        game['game_slug'] = slug
        
    user=UserProfile.objects.get(user=user)
    user.revenue = revenue
    if user.isRevenuePrivate and request.user.username != username:
        revenue = "$$$$"
    else:
        revenue = f"${revenue}"
    
    recentlyPlayedGames = list(recentlyPlayedGames.values())        
    for game in recentlyPlayedGames:
        avatar = Game.objects.get(id=game['game_id']).image.url
        title = Game.objects.get(id=game['game_id']).title
        slug = Game.objects.get(id=game['game_id']).slug
        game['game_avatar'] = avatar
        game['game_title'] = title
        game['game_slug'] = slug
        
    print("recentlyPlayedGames")
    print(recentlyPlayedGames)
    
    context = {'username': user.user.username, 'email': email,
                         'nickname': user.nickname, 'avatar': user.avatar.url,
                         'bio': user.bio,
                         'header': user.header.url,"isCurrentUser":
                             request.user.is_authenticated and request.user.username == username,
                             "playedGames":playedGames,"NumberOfListedGames":NumberOfListedGames,"revenue":revenue,
                             "isRevenuePrivate":user.isRevenuePrivate,   
                             "recentlyPlayedGames":recentlyPlayedGames, 
                             "mylistedGames":mylistedGames,
                             "reviews": getReviews(username)['reviews']                        
                              }
    return JsonResponse(context)


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
        user.isRevenuePrivate=True if request.POST.get('isRevenuePrivate')=="private" else user.isRevenuePrivate==False
        user.save()
        return JsonResponse({'username': user.user.username, 'email': user.user.email,
                         'nickname': user.nickname, 'avatar': user.avatar.url,
                         'bio': user.bio,
                         'header': user.header.url,})
    else:
        return JsonResponse({'status': "Use POST method"})
        
        
        



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
    
    
def isFav(request,slug):
    if request.user.is_authenticated and request.method == 'GET' :
        game=Game.objects.get(slug=slug)
        user=AuthUser.objects.get(username=request.user.username)
        user=UserProfile.objects.get(user=user)
        if user.games.filter(slug=slug).exists():
            return JsonResponse({'status': "success"})
        else:
            return JsonResponse({'status': "fail"})
        
    else:
        return JsonResponse({'status': "Use GET method"})
    
    
def addComment(request, game_slug):
    if request.user.is_authenticated and request.method == 'POST':
        game = Game.objects.get(slug=game_slug)
        user = AuthUser.objects.get(username=request.user.username)

        try:
            data = json.loads(request.body)
            review_text = data.get('review')
            rating = data.get('rating')
            print(data)
            review = Reviews(user=user, game=game, review=review_text, rating=rating)
            review.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'fail'})
    else:
        return JsonResponse({'status': 'Use POST method'})
    
    
def getAvatar(request,id):
    user=AuthUser.objects.get(id=id)
    user=UserProfile.objects.get(user=user)
    print(user.avatar.url)
    return JsonResponse({'avatar': user.avatar.url})

def getReviews(user):
    try:
        user = AuthUser.objects.get(username=user)
        reviews = RateStreamerModel.objects.filter(streamer=user)
        review_list = []

        for review in reviews:
            review_info = {
                'content': review.content,
                'rating': review.rating,
                'user': review.user.username,
                'user_avatar': review.user.userprofile.avatar.url,
                'game_slug': review.game.slug,
                'user_nickname': review.user.userprofile.nickname,
                'game_title': review.game.title,
            }
            review_list.append(review_info)

        return {'reviews': review_list}
    
    except Exception as e:
        print(e)
        return {'reviews': []}
    