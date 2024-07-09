from django.db import models
from category_app.models import *
from brand_app.models import *
from django.urls import reverse

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='images/products_img')
    stock = models.IntegerField()

    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('product_details',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
