from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
import datetime

class Game(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, default=slugify(title))
    genre = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    owners = models.ManyToManyField(User, blank=True, related_name='owners', default=5)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.TextField(blank=True, null=True, default='')
    nickname = models.CharField(max_length=255, blank=True, null=True, default='')
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png')
    header = models.ImageField(upload_to='header/', default='header/default.png')
    games = models.ManyToManyField(Game, blank=True, related_name='user_games', default=None)
    for_rent = models.JSONField(blank=True, null=True)  # JSONField is a dictionary <game:PricePerHour>
    revenue = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    isRevenuePrivate = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
import random
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    rented_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='rented_transactions')
    randomNumber = models.IntegerField(default=random.randint(1000000000, 999999999999), unique=True)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='game_transactions')
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start_date= models.DateField(default=datetime.date.today)
    start_hour = models.TimeField(default=datetime.datetime.now)
    end_hour = models.TimeField(default=datetime.datetime.now)
    is_paid = models.BooleanField(default=False)
    invoiceId= models.CharField(max_length=255, blank=True, null=True, default='')
    session_id = models.URLField(max_length=255, blank=True, null=True, default='')
    isitToday= models.BooleanField(default=False)
    isPlayable= models.BooleanField(default=False)
    isPlayed= models.BooleanField(default=False)
    notExpied= models.BooleanField(default=False)
    isRated = models.BooleanField(default=False)
    revenue= models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.game.title} - {self.price_per_hour} - {self.start_date} - {self.start_hour} - {self.end_hour} - {self.is_paid}"
     


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField()
    starting_time = models.TimeField(blank=True, null=True, default='')
    ending_time = models.TimeField(blank=True, null=True, default='')

    
    def __str__(self):
        return f"{self.id}--{self.game.title} - {self.user.username} - {self.start} to {self.end} - {self.price_per_hour}"


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()



class RateStreamerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, related_name='game')
    streamer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streamer')
    rating = models.IntegerField()
    content = models.TextField()