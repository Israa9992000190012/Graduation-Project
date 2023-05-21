from django.db import models
import uuid
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.

class BillingAddress(models.Model):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = 'Billing Address'
        

class Payment(models.Model):

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, default='Visa')
    card_number = models.CharField(max_length=50)
    exp_month = models.CharField(max_length=50)
    exp_year = models.CharField(max_length=50)
    cvv = models.CharField(max_length=50)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.payment_method
    
    class Meta:
        verbose_name_plural = 'Payment'


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() # Quantity of product -> how many products are ordered
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending', choices=STATUS) 
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Order'


class OrderItem(models.Model):
    order_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() # Quantity of order item -> انت عامل كام اوردر
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name_plural = 'Order Item'


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Cart'


