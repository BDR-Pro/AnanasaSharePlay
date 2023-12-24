from django.shortcuts import render, redirect
from shareplay.models import Game , UserProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from urllib.parse import unquote

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