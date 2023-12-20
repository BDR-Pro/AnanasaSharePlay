# shareplay/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
class Game(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True,default=slugify(title))
    genre = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    owner = models.JSONField(blank=True, null=True)  # JSONField is a dictionary <owner:PricePerHour>
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    nickname= models.CharField(max_length=255, blank=True, null=True, default='')
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png')
    games = models.ManyToManyField(Game, blank=True, related_name='user_games',default=None)
    for_rent = models.JSONField(blank=True, null=True)  # JSONField is a dictionary <game:PricePerHour>

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    rented_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_transactions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
