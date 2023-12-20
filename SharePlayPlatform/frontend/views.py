from django.shortcuts import render, redirect
from shareplay.models import Game
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def detail(request,slug, *args, **kwargs):
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