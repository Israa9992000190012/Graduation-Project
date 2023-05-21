from django.contrib import admin
from .models import BillingAddress, Payment, Order, OrderItem, Cart

# Register your models here.
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)

