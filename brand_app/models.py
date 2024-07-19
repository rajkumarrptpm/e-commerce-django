from django.db import models
from django.urls import reverse

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length = 50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/brand_img',blank=True)


    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def get_url(self):
        return reverse('store_app:products_by_brands', args=[self.slug])

    def __str__(self):
        return self.brand_name