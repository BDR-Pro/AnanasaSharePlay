from django.shortcuts import render, redirect
from shareplay.models import Game , UserProfile , listing
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from datetime import datetime, timezone

from django.db.models import Avg

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def detail(request,slug):

    if request.method == 'POST':
        if request.user.is_authenticated:
            game = get_object_or_404(Game, slug=slug)
            user = get_object_or_404(UserProfile, user=request.user)
            user.games.add(game)
            return JsonResponse({'status':'success'})
        else:
            return redirect('/login')
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            game = get_object_or_404(Game, slug=slug)
            user = get_object_or_404(UserProfile, user=request.user)
            user.games.remove(game)
            return JsonResponse({'status':'success'})
        else:
            return redirect('/login')
    if request.method == 'GET':    
        game = get_object_or_404(Game, slug=slug)
    return render(request, 'frontend/detail.html',{"game": game})

def login(request, *args, **kwargs):
    return render(request, 'frontend/login.html')

def register(request, *args, **kwargs):
    return render(request, 'frontend/register.html')

def search(request, *args, **kwargs):
    query=request.GET.get('query')
    games = Game.objects.all().filter(title__icontains=query)
    return render(request, 'frontend/search.html',{"games": games, "query": query})

def Profile(request, *args, **kwargs):
    if request.user.is_authenticated:
        user = request.user
        return redirect(f'/users/{user}',{"user": user})
    else:
        return redirect('/login')
    
    
def MyGames(request):
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, user=request.user)
        games = user.games.all()
        return render(request, 'frontend/mygames.html',{"games": games})
    else:
        return redirect('/login')
    
    
def genre(request,slug):
    slug=unquote(slug)
    print(slug)
    games = Game.objects.all().filter(genre__icontains=slug)
    return render(request, 'frontend/genre.html',{"games": games, "slug": slug})

def renting(request, slug):
    link = request.get_full_path()
    
    if request.user.is_authenticated:
        if request.method == 'GET':
            game = get_object_or_404(Game, slug=slug)
            games = Game.objects.all()
            listed = listing.objects.filter(game=game, is_available=True, start__gt=datetime.now(timezone.utc))
            listed = sorted(listed, key=lambda x: x.start)
            
            listed_games = []
            for item in listed:
                user_profile = UserProfile.objects.get(user_id=item.user_id)
                listed_games.append({
                    'game_title': game.title,
                    'price_per_hour': item.price_per_hour,
                    'start': item.start.date(),
                    'end': item.end.date(),
                    'starting_time': item.starting_time,
                    'ending_time': item.ending_time,
                    'is_available': item.is_available,
                    'user':item.user,
                    'avatar': user_profile.avatar.url,
                    'nickname': user_profile.nickname,
                })

            avg_price = listing.objects.filter(game=game).aggregate(Avg('price_per_hour'))
            hours = [f"{i:02d}:00" for i in range(24)]
            
            return render(request, 'frontend/renting.html', {
                "slug": slug,
                "mygame": game,
                "listedGames": listed_games,
                "games": games,
                "avgPrice": avg_price,
                "hours": hours,
            })
            
        if request.method == 'POST':
            game=get_object_or_404(Game, slug=slug)
            print(request.POST)
            '''
            game	"2"
            price_per_hour	"15"
            start	"2023-12-25"
            start_hour	"01:00"
            end	"2024-01-03"
            end_hour	"12:00"
            
            '''
            
            listed=listing.objects.create(user=request.user,game=game,price_per_hour=request.POST['price_per_hour'],
                                          start=request.POST['start'],end=request.POST['end'],
                                          starting_time=request.POST['start_hour'],ending_time=request.POST['end_hour'])
            user = get_object_or_404(UserProfile, user=request.user)
            # Assuming you have the User instance as user and the game and listed instances
            # game and listed should be instances of the Game and Listing models, respectively

            # Retrieve the existing for_rent dictionary from the user
            for_rent_dict = user.for_rent or {}

            # Update the dictionary with the new game and its price per hour
            for_rent_dict[game.id] = listed.price_per_hour

            # Update the User instance with the modified for_rent dictionary
            user.for_rent = for_rent_dict

            user.save()
            
            
            return redirect(link)
        
    else:
        return redirect('/login')