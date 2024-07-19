from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store_app.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)

    category_slug = product.category.slug  # Assuming your product model has a related category with a slug field
    product_slug = product.slug  # Assuming your product model has a slug field

    # variation
    product_variation = []
    if request.method == 'POST':

        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass


    product_variations_exist = Variation.objects.filter(product=product).exists()
    if product_variations_exist and not product_variation:
        # return redirect('store_app:product_details', category_slug=category_slug, product_slug=product_slug)
        pass
    else:

        #Cart
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        # Cart Item
        is_cart_item_exist =CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variation -> database
            # current variation -> product_variation
            # item id -> database
            ex_var_list = []
            id=[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in ex_var_list:
                # increase the cart_item quantity
                index = ex_var_list.index(product_variation)
                print(index)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
                pass
            else:
                # create new cart item
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )

            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    return redirect('store_app:product_details', category_slug=category_slug, product_slug=product_slug)

def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products,id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:

            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
            total += (cart_item.product.price * cart_item.quantity)
        tax = round((9*total)/100,2)
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total':grand_total

    }
    # return HttpResponse(total)
    return render(request, 'store/cart.html',context)
