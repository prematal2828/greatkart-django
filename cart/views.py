from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product


# Create your views here.


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()

    return cart_id


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_id = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart_id = Cart.objects.create(cart_id=_cart_id(request))
        cart_id.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart_id=cart_id,
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart_id = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart_id = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart_id = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity

        tax = total * 2 / 100
        grand_total = total + tax

    except:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)
