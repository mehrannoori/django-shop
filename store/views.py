from django.shortcuts import render
import json
from django.http import JsonResponse

from .models import Product, Cart, CartItem



def store_index(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'store.html', context)



def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)
        
    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartItem, cartItem_created = CartItem.objects.get_or_create(product=product, cart=cart)
        cartItem.quantity += 1
        cartItem.save()

    return JsonResponse("Ok", safe=False)