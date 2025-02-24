from django.shortcuts import render

from store.models import Cart

def HomePageView(request):
    if request.user.is_authenticated:
        cart, created_cart = Cart.objects.get_or_create(user=request.user, completed=False)
    context = {'cart': cart}

    return render(request, 'home.html', context=context)