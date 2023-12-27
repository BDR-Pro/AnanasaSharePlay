from django.shortcuts import render, redirect
from shareplay.models import Game , UserProfile , Listing, Transaction , Reviews
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.db.models import Avg
from datetime import datetime, timezone
from django.db.models import Avg
from django.core.exceptions import PermissionDenied
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime
from django.conf import settings
import stripe
from django.core.serializers import serialize



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
        NumberOfRenters=Transaction.objects.filter(game=game).count()
        NumberOfFavorites=UserProfile.objects.filter(games=game).count()
        NumberOfStreamers=Listing.objects.filter(game=game).count()
        NumberOfOwners=game.owners.count()
        game.views += 1
        views=game.views
        NumberOfComments=Reviews.objects.filter(game=game).count()
        AvgRating=Reviews.objects.filter(game=game).aggregate(Avg('rating'))['rating__avg']
        game = serialize('json', [game])
        context = {
            "game": game,
            "views": views,
            "NumberOfRenters": NumberOfRenters,
            "NumberOfFavorites": NumberOfFavorites,
            "NumberOfStreamers": NumberOfStreamers,
            "NumberOfOwners": NumberOfOwners,
            "NumberOfComments": NumberOfComments,
            "AvgRating": AvgRating,
            
        }
        print("context")
        print(context)
    return render(request, 'frontend/detail.html',{"context":context})

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
                    'user':item.user,
                    'avatar': user_profile.avatar.url,
                    'nickname': user_profile.nickname,
                })

            avg_price = Listing.objects.filter(game=game).aggregate(Avg('price_per_hour'))


            return render(request, 'frontend/renting.html', {
                "slug": slug,
                "mygame": game,
                "listedGames": listed_games,
                "games": games,
                "avgPrice": avg_price,
           
            })
            
        if request.method == 'POST':
            game=get_object_or_404(Game, slug=slug)
            print(request.POST)
            '''
            game	"2"
            price_per_hour	"15"
            start	"2023-12-25"
            starting_hour	"01:00"
            end	"2024-01-03"
            ending_hour	"12:00"
            
            '''

            
            current_date = datetime.now(timezone.utc).date()
            start_hour = request.POST['starting_hour']
            end_hour = request.POST['ending_hour']
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
            avgPrice = Listing.objects.filter(game=game).aggregate(Avg('price_per_hour'))['price_per_hour__avg']
            return render(request, 'frontend/rent-your-game.html', {"listed": listed, "streamer": streamer, "game": game,
                                                                "avgPrice": avgPrice})

        if request.method == 'POST':
            listed = get_object_or_404(Listing, id=id)

            # Assuming your form includes a field 'selected_start' and 'selected_end' representing the selected time range
            selected_start = request.POST.get('selected_start')
            start_hour = request.POST.get('start')
            end_hour = request.POST.get('end')
            print(request.POST)

            if is_time_range_available(listed, selected_start,start_time=start_hour, end_time=end_hour):
                print(listed.user)
                print(request.user)
                print(listed.game)                
                '''
                
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    rented_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_transactions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField(default=datetime.datetime.now)
    is_paid = models.BooleanField(default=False)
     
     
                
                '''
                initTransaction = Transaction.objects.create(
                    user=listed.user,
                    rented_user=request.user,
                    game=listed.game,
                    price_per_hour=listed.price_per_hour,
                    start_date=selected_start,
                    start_hour=start_hour,  
                    end_hour=end_hour      
                )
                return redirect('/Profile/rents')
            else:
                raise PermissionDenied  

def is_time_range_available(listed: Listing,startDate, start_time, end_time):
    # Combine the start_date with start_time and end_time to create datetime objects
    '''
    

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField()
    starting_time = models.TimeField(blank=True, null=True, default='')
    ending_time = models.TimeField(blank=True, null=True, default='')
    
    '''
    print("is_time_range_available")
    print(listed)
    print("start_date")
    print(startDate)
    print("start_time")
    print(start_time)
    print("end_time")
    print(end_time)
    startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()
    if startDate < datetime.now(timezone.utc).date():
        return False
    if start_time > end_time:
        return False
    if start_time == end_time:
        return False
    if start_time < datetime.now(timezone.utc).time():
        return False
    if end_time < datetime.now(timezone.utc).time():
        return False
    if startDate < listed.start.date():
        return False
    if startDate > listed.end.date():
        return False
    
    
    

    # Query transactions for the same user, game, and date
    overlapping_transactions = Transaction.objects.filter(
        user=listed.user,
        game=listed.game,
        start_date=listed.start,  # Filter transactions for the same date
        start_hour__lte=start_time,  # Filter transactions with a start_hour less than or equal to the selected start_time
        end_hour__gte=end_time  # Filter transactions with an end_hour greater than or equal to the selected end_time
    )
    
    start_datetime = datetime.combine(listed.start, start_time)
    end_datetime = datetime.combine(listed.start, end_time)

    # Check for overlap with existing transactions
    for transaction in overlapping_transactions:
        transaction_start = datetime.combine(transaction.start_date, transaction.start_hour)
        transaction_end = datetime.combine(transaction.start_date, transaction.end_hour)

        if (start_datetime < transaction_start < end_datetime) or \
           (start_datetime < transaction_end < end_datetime):
            return False  # Overlapping time range, not available

    return True  # No overlap found, the time range is available


def rents(request):
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, user=request.user)
        transactions = Transaction.objects.filter(rented_user=user.user).order_by('-start_date').order_by('start_hour')
        return render(request, 'frontend/rents.html',{"transactions": transactions})
    else:
        return redirect('/login')
from decimal import Decimal

def pay(request, randomNumber):
    if request.user.is_authenticated:
        transaction = get_object_or_404(Transaction, randomNumber=randomNumber)
        # Calculate the number of hours
        start_datetime = datetime.combine(transaction.start_date, transaction.start_hour)
        end_datetime = datetime.combine(transaction.start_date, transaction.end_hour)
        time_difference = end_datetime - start_datetime
        number_of_hours = time_difference.total_seconds() / 3600
        # Convert number_of_hours to Decimal
        number_of_hours = Decimal(str(number_of_hours))
        if number_of_hours < 1:
            number_of_hours = 1
        # Set your secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        pricetag=int(transaction.price_per_hour * number_of_hours * 100)
        print(pricetag)
        try:
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=pricetag,
                currency='usd',
                description=f'Payment for {transaction.game.title}',
                payment_method_types=['card'],
            )

            client_secret = payment_intent.client_secret

            # Save the transaction after successful payment
            transaction.save()
            pricetag=float(pricetag)
            pricetag=pricetag/100
            pricetag = "{:.2f}".format(pricetag)
            context = {
                
                    'client_secret': client_secret,
                    'total_amount': pricetag,
                    'game_title': transaction.game.title,
                    'start_date': transaction.start_date,
                    'start_hour': transaction.start_hour,
                    'end_hour': transaction.end_hour,
                    'price_per_hour': transaction.price_per_hour,
                    'random_number': transaction.randomNumber,
                }

            
            return render(request, 'frontend/payment.html', context)
        except stripe.error.CardError as e:
            # Handle card errors
            error_msg = str(e.error)
            return render(request, 'frontend/payment.html', {'error_msg': error_msg})
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            error_msg = "An error occurred. Please try again later."
            return render(request, 'frontend/payment.html', {'error_msg': error_msg})
    else:
        return redirect('/login')



def check_invoice_payment_status(request):
    try:
        invoiceId = request.POST.get('invoiceId')
        transactionId = request.POST.get('transactionId')
        Transaction = get_object_or_404(Transaction, id=transactionId)
        invoice = stripe.Invoice.retrieve(invoiceId)
        Transaction.invoiceId = invoiceId
        print(request.POST)
        if invoice.payment_status == 'paid':
            Transaction.is_paid = True
            return True
        else:
            return False

    except stripe.error.StripeError as e:
        # Handle any Stripe API errors
        print(f"Stripe error: {e}")
        return False
    
