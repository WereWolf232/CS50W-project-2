from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)

class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

class Listing(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_price = models.DecimalField(decimal_places=2, max_digits=8)
    current_bid = models.ForeignKey(Bid, on_delete=models.PROTECT, null=True, blank=True, )
    image = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64)
    ongoing = models.BooleanField(default=True)


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    person = models.ForeignKey(User, on_delete=models.CASCADE)



