from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib import messages
import uuid
from django.contrib.auth import authenticate, login

from .models import Product, Cart, CartItem



def store_index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store.html', context)


def cart(request):
    context = {}
    return render(request, 'cart.html', context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, cartitem_created = CartItem.objects.get_or_create(product=product, cart=cart)
        cartitem.quantity += 1
        cartitem.save()
        num_of_items = cart.num_of_items
    else:
        try:
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
            cartitem, cartitem_created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_items = cart.num_of_items
        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id=request.session['nonuser'], completed=False)
            cartitem, cartitem_created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_items = cart.num_of_items
        # num_of_items = cart.num_of_items
        # print(cartitem)
    return JsonResponse(num_of_items, safe=False)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
                if Cart.objects.filter(user=request.user, completed=False).exists():
                    cart.user = None
                    cart.save()
                else:
                    cart.user = request.user
                    cart.save()
            except:
                print("WTF?")
        return redirect('store')
    else:
        print('Invalid credential provided')
    context = {}
    return render(request, 'login.html', context)

    


def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("store")
    # return JsonResponse('Ok', safe=False)