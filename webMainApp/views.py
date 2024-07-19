from django.shortcuts import render,redirect
from store_app.models import Products

# Create your views here.

def home(request):
    products=Products.objects.all().filter(is_available = True)

    context = {
        'products': products,
        'active_page':'home',
    }
    return render(request ,'index.html', context)