from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()

    return cart_id


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart_id = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart_id = Cart.objects.create(cart_id=_cart_id(request))
        cart_id.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart_id=cart_id).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart_id=cart_id)
        existing_variation_list = []
        ids = []
        for i in cart_item:
            existing_variation = i.variations.all()
            existing_variation_list.append(list(existing_variation))
            ids.append(i.id)

        if product_variation in existing_variation_list:
            index = existing_variation_list.index(product_variation)
            existing_cart_item_id = ids[index]
            existing_cart_item = CartItem.objects.get(product=product,
                                                      id=existing_cart_item_id)
            existing_cart_item.quantity += 1
            existing_cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart_id=cart_id,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart_id=cart_id,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart_id = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart_id=cart_id, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart_id = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart_id=cart_id, id=cart_item_id)
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

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)
