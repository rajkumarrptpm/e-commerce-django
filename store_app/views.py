from django.shortcuts import render, get_object_or_404
from .models import *
from category_app.models import *
from brand_app.models import *
# Create your views here.


def shop(request,category_slug=None,brand_slug=None):
    categories = None
    brands =None
    products = None
    if category_slug != None or brand_slug!=None:
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Products.objects.filter(category=categories,is_available=True)
            product_count = products.count()
        if brand_slug!=None:
            brands = get_object_or_404(Brand, slug=brand_slug)
            products = Products.objects.filter(brand=brands, is_available=True)
            product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request,'store/shop.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Products.objects.get(category__slug = category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context ={
        'single_product':single_product,

    }
    return render(request,'store/product_detail.html',context)
