from django.urls import path
from . import views
import random

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/billing-address-and-payment-information/', views.get_billing_address_and_payment_information, name='billing-address-and-payment-information'),
]