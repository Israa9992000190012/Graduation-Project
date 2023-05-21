from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, BillingAddress, Payment, Order
from product.models import Product
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart.quantity += 1
        cart.save()
    messages.success(request, 'Product added to cart successfully')
    return redirect('cart')


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user) #returns a list of cart items

    total_price = 0
    # loop through cart items and calculate total price
    try:
        for item in cart_items:
            total_price += item.product.product_price * item.quantity
    except TypeError:
        # to avoid TypeError: unsupported operand type(s) for +: 'str' and 'int'
        # handle the error
        for item in cart_items:
            total_price += int(item.product.product_price) * item.quantity

    tax = 0.05 * total_price
    shipping_cost = 2
    grand_total = total_price + tax + shipping_cost


    return render(request, 'payment/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'tax': tax, 'shipping_cost': shipping_cost, 'grand_total': grand_total})


@login_required(login_url='login')
def remove_from_cart(request, pk):

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart = get_object_or_404(Cart, user=request.user, product=product)
        cart.delete()
        messages.success(request, 'Product removed from cart successfully')
        return redirect('cart')
    
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    return render(request, 'payment/payment.html')

import re


# start of payment views and order views
@login_required(login_url='login')
def get_billing_address_and_payment_information(request):
    if request.method == 'POST':
        billing_address = BillingAddress(
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],
        )

        card_number = request.POST['card_number']
        cvv = request.POST['cvv']

        # validate card number
        if not re.match(r'^[0-9]{16}$', card_number):
            messages.error(request, 'Invalid card number')
            return redirect('checkout')
        
        # validate cvv
        if not re.match(r'^[0-9]{3}$', cvv):
            messages.error(request, 'Invalid cvv')
            return redirect('checkout')
        
        # save billing address and payment information
        payment = Payment(
            user=request.user,
            payment_method=request.POST['payment_method'],
            card_number= card_number,
            exp_month=request.POST['exp_month'],
            exp_year=request.POST['exp_year'],
            cvv=cvv,
            billing_address=billing_address,
        )
        billing_address.save()
        payment.save()

        # add to order
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            order = Order(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                payment=payment,
                billing_address=billing_address,
            )
            order.save()
            item.delete() # delete cart item after adding to order
                
        messages.success(request, 'Order placed successfully')
        return redirect('cart')
    
    return redirect('checkout')

