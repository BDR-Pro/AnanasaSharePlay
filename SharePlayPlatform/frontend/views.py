from django.shortcuts import render, redirect
from shareplay.models import Game , UserProfile , Listing, Transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.db.models import Avg
from datetime import datetime, timezone
from django.db.models import Avg
from .utils import is_time_range_available, mark_time_range_unavailable
from django.core.exceptions import PermissionDenied
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime





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
            listed = Listing.objects.filter(game=game)
            print(listed)
            print("before-------filter") 
            listed = Listing.objects.filter(game=game, end__gte=datetime.now(timezone.utc))
            print(listed)
            
            print("before sorted")
            listed = sorted(listed, key=lambda x: x.start)
            print(listed)            
            listed_games = []
            for item in listed:
                user_profile = UserProfile.objects.get(user_id=item.user_id)
                listed_games.append({
                    'id': item.id,
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

            avg_price = Listing.objects.filter(game=game).aggregate(Avg('price_per_hour'))
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
            msg=''
            if request.POST['start'] > request.POST['end']:
                msg='Start date must be before end date'
                return redirect(link, msg=msg)
            if request.POST['start'] == request.POST['end']:
                if request.POST['start_hour'] > request.POST['end_hour']:
                    msg='Start time must be before end time'
                    return redirect(link, msg=msg)
            if request.POST['start'] == request.POST['end']:
                if request.POST['start_hour'] == request.POST['end_hour']:
                    msg='Start time must be before end time'
                    return redirect(link, msg=msg)
            if request.POST['price_per_hour'] == '':
                msg='Price per hour must be filled'
                return redirect(link, msg=msg)
            if request.POST['start'] == '':
                msg='Start date must be filled'
                return redirect(link, msg=msg)
            if request.POST['end'] == '':
                msg='End date must be filled'
                return redirect(link, msg=msg)
            if request.POST['start_hour'] == '':
                msg='Start time must be filled'
                return redirect(link, msg=msg)
            if request.POST['end_hour'] == '':
                msg='End time must be filled'
                return redirect(link, msg=msg)
            
            
            current_date = datetime.now(timezone.utc).date()
            start_hour = request.POST['start_hour']
            end_hour = request.POST['end_hour']
            # Construct start and end datetime objects using the current date and selected hours
            start_datetime = timezone.make_aware(datetime.combine(current_date, datetime.strptime(start_hour, '%H:%M').time()))
            end_datetime = timezone.make_aware(datetime.combine(current_date, datetime.strptime(end_hour, '%H:%M').time()))
            print(start_datetime)
            print(end_datetime)
            
            # Create the Listing object
            listed = Listing.objects.create(
                user=request.user,
                game=game,
                price_per_hour=request.POST['price_per_hour'],
                start=start_datetime,
                end=end_datetime,
                starting_time=start_hour,
                ending_time=end_hour
            )
            
            print(listed)

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



def RentYourGame(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            listed = get_object_or_404(Listing, id=id)
            streamer = get_object_or_404(UserProfile, user=listed.user)
            game = get_object_or_404(Game, id=listed.game.id)
            hours = [f"{i:02d}:00" for i in range(24)]
            avgPrice = Listing.objects.filter(game=game).aggregate(Avg('price_per_hour'))['price_per_hour__avg']
            return render(request, 'frontend/rent-your-game.html', {"listed": listed, "streamer": streamer, "game": game,
                                                                    "hours": hours, "avgPrice": avgPrice})

        if request.method == 'POST':
            listed = get_object_or_404(Listing, id=id)

            # Assuming your form includes a field 'selected_start' and 'selected_end' representing the selected time range
            selected_start = request.POST.get('selected_start')
            selected_end = selected_start 
            start_hour = request.POST.get('start_hour')
            end_hour = request.POST.get('end_hour')
            print(request.POST)

            if is_time_range_available(listed, selected_start, selected_end):
                mark_time_range_unavailable(listed, selected_start, selected_end)
                print(listed.user)
                print(request.user)
                print(listed.game)                
                
                initTransaction = Transaction.objects.create(
                    user=listed.user,
                    rented_user=request.user,
                    game=listed.game,
                    price_per_hour=listed.price_per_hour,
                    start=selected_start,
                    start_hour=start_hour,  
                    end_hour=end_hour      
                )
                return redirect('/Profile/rents')
            else:
                raise PermissionDenied  # Raise PermissionDenied instead of 403
            
            