from django.shortcuts import render, get_object_or_404

from category.models import Category
from store.models import Product


# Create your views here.

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.all().filter(product_category=category, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(product_category__category_slug=category_slug, product_slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product
    }

    return render(request, 'product_details.html', context)