from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.

def store(request, category_slug=None):
    # category = None
    # products = None

    if category_slug is not None:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.all().filter(product_category=category, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(product_category__category_slug=category_slug, product_slug=product_slug)
        in_cart = CartItem.objects.filter(cart_id__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }

    return render(request, 'product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.all().filter(is_available=True).order_by('created_date').filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()

            context = {
                'products': paged_products,
                'product_count': product_count,
            }
            return render(request, 'store.html', context)

    return render(request, 'store.html')



