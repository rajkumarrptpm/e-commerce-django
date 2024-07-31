import datetime

from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import *

from cart_app.models import CartItem
from .models import Order


# Create your views here.
def confirm_order(request):
    current_user = request.user
    status = {
        "confirmed": "confirmed"
    }

    order = Order.objects.get(user=current_user, is_ordered=False)

    confirm_order = Confirm_order(
        user=current_user,
        order_id=order.order_number,  # Changed from order_id to order object
        amount=order.order_total,
        status=status['confirmed']
    )

    confirm_order.save()
    order.is_ordered = True
    order.save()

    # move the cart_item to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.corfirmed_order_id = confirm_order
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        # reduce the quantity of sold products
        product = Products.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # send order recieved email to customer
    mail_subject = 'Thank you for Shopping with us'
    message = render_to_string('order/order_received_email.html', {
        'user': request.user,
        'order': order,

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # send order number

    return redirect(f'/orders/order_complete/?order_id={order.order_number}')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round((9 * total) / 100, 2)
    grand_total = total + tax

    if request.method == "POST":

        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside the table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.mobile_no = form.cleaned_data['mobile_no']
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.street = form.cleaned_data['street']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_num = current_date + str(data.id)
            data.order_number = order_num
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_num)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total

            }
            return render(request, 'order/confirm.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_id = request.GET.get('order_id')

    try:
        order = Order.objects.get(order_number=order_id, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)
        sub_total = 0
        grand_total=0
        for i in ordered_products:
            sub_total+=(i.price*i.quantity)
        tax = round((9 * sub_total) / 100, 2)
        grand_total = sub_total + tax
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'sub_total': sub_total,
            'tax': tax,
            'grand_total': grand_total,

        }
        return render(request, 'order/order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('home')


