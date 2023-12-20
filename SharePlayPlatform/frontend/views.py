from django.shortcuts import render
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