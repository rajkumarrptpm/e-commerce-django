from django.shortcuts import render, redirect

from store_app.models import *
from wishlist_app.models import *


# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(
            wishlist_id=_wishlist_id(request)
        )
    wishlist.save()

    try:
        wishlist_item = WishlistItem.objects.get(product=product, cart=cart)
        wishlist_item.quantity += 1
        wishlist_item.save()
    except WishlistItem.DoesNotExist:
        cart_item = WishlistItem.objects.create(
            product=product,
            quantity=1,
            wishlist=wishlist,
        )
        cart_item.save()
    return redirect('wishlist')
def wishlist(request):
    return render(request,'store/wishlist.html')

