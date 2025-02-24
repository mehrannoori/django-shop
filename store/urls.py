from django.urls import path

from . import views

urlpatterns = [
    path('', views.store_index, name='store'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]