from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    cat_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.cat_name}"

class Listings(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    imageUrl = models.CharField(max_length=1000, default="")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlistListing")

    def __str__(self):
        return f"{self.id}: {self.title}, {self.description}, {self.price}, {self.imageUrl}"

class Bids(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidOwner")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    bid = models.FloatField()

