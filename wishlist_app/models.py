from django.db import models
from store_app.models import *

# Create your models here.
class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id


class WishlistItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product