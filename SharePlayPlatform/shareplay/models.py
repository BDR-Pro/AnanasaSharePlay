# shareplay/models.py

from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    owner = models.JSONField(blank=True, null=True)  # JSONField is a dictionary <owner:PricePerHour>

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField() 
    nickname = models.CharField(max_length=255)
    games = models.ManyToManyField(Game)
    for_rent = models.JSONField(blank=True, null=True)  # JSONField is a dictionary <game:PricePerHour>

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    rented_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_transactions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
