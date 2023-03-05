from django.db import models
from django.urls import reverse

from category.models import Category


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    product_slug = models.SlugField(max_length=255, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='photos/products')
    product_stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_details', args=[self.product_category.category_slug, self.product_slug])

    def __str__(self):
        return self.product_name
