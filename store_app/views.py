from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cart_app.models import *
from cart_app.views import _cart_id
from .models import *
from category_app.models import *
from brand_app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def shop(request, category_slug=None, brand_slug=None):
    categories = None
    brands = None
    products = None
    if category_slug or brand_slug :
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Products.objects.filter(category=categories, is_available=True)

        if brand_slug:
            brands = get_object_or_404(Brand, slug=brand_slug)
            products = Products.objects.filter(brand=brands, is_available=True)

        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
        'active_page': 'shop',
        'categories':categories,
        'brands':brands,

    }
    return render(request, 'store/shop.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)



def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products=Products.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count = products.count()
    context={

        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/shop.html',context)


def contact(request):
    context = {
        'active_page':'contacts'
    }
    return render(request, 'store/contact.html',context)