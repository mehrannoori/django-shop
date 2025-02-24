from django.shortcuts import render
import json
from django.http import JsonResponse

from .models import Product, Cart, CartItem



def store_index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        cart, created_cart = Cart.objects.get_or_create(user=request.user, completed=False)

    context = {'products': products, 'cart': cart}

    return render(request, 'store.html', context)


def cart(request):

    cart = None
    cartitems = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {"cart": cart, "items": cartitems}

    return render(request, 'cart.html', context=context)

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)
        
    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartItem, cartItem_created = CartItem.objects.get_or_create(product=product, cart=cart)
        cartItem.quantity += 1

        cartItem.save()
        num_of_items = cart.num_of_items


    return JsonResponse(num_of_items, safe=False)