from .models import *


def brand_links(request):
    link = Brand.objects.all()
    return dict(links=link)