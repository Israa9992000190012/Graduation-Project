from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from product.models import Product
from payment.models import Order
from review_blog.models import NLPReviewStored
from django.contrib.auth.decorators import login_required
from .models import Message
# import group
from django.contrib.auth.models import Group


#import messages
from django.contrib import messages

###########################################
from product.models import Product
from payment.models import Order


from django.db.models import Q
from django.views.decorators.http import require_GET
# import order_set for each order
from django.db.models import Prefetch



def admin_register(request):
    if request.user.is_authenticated:
        return redirect('d-index')
    else:
        # get the data from frontend admin
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # check if the passwords match
            if password1 == password2:
                # check if the username is taken
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is taken')
                    return redirect('admin-register-oAuth')
                # check if the email is taken
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is taken')
                    return redirect('admin-register-oAuth')
                else:
                    # create user
                    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                    
                    # add user to admin group
                    group = Group.objects.get(name='admin')
                    user.groups.add(group)
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    messages.success(request, 'Admin is now registered and can log in')
                    return redirect('admin-login-oAuth')
            else:
                messages.info(request, 'Password not matching')
                return redirect('admin-register-oAuth')
        else:
            # if the request is not POST
            pass
    
    return render(request, 'admin-auth/register.html')



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('d-index')
    else:
        # get the data from frontend admin
        if request.method == 'POST':
            # check if the user is in the admin group
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username=username).first()
            if user is not None:
                if user.groups.filter(name='admin').exists():
                    user = authenticate(request, username=username, password=password)
                    if user is not None: 
                        login(request, user)
                        messages.success(request, 'You are now logged in')
                        return redirect('d-index')
                    else:
                        messages.info(request, 'Invalid credentials')
                        return redirect('admin-login-oAuth')
                else:
                    messages.info(request, 'You are not an admin')
                    return redirect('admin-login-oAuth')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('admin-login-oAuth')
        else:
            # if the request is not POST
            pass
    
    return render(request, 'admin-auth/login.html')

@login_required(login_url='admin-login-oAuth')
def index(request):
    products = Product.objects.all()
    product_count = products.count()
    # get total earnings
    orders = Order.objects.all() # type: ignore
    total_earnings = 0
    for order in orders:
        total_earnings += int(order.product.product_price)

    users = User.objects.all()
    total_users = User.objects.all().exclude(is_superuser=True).count()
    total_orders = Order.objects.all().count()
    context = {
        'products': products,
        'product_count': product_count,
        'total_users': total_users,
        'total_earnings': total_earnings,
        'users': users,
        'total_orders': total_orders,
    }
    return render(request, 'pages/index.html', context)


@login_required(login_url='admin-login-oAuth')
def products(request):
    products = Product.objects.all()
    return render(request, 'pages/products.html', {'products': products})

@login_required(login_url='admin-login-oAuth')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('d-products')


@login_required(login_url='admin-login-oAuth')
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
        product.quantity_available = request.POST['quantity_available']
        product.product_material = request.POST['product_material']
        product.product_image = request.FILES['product_image']
        product.save()
        return redirect('d-products')
    return render(request, 'pages/update_product.html', {'product': product})



@login_required(login_url='admin-login-oAuth')
def orders(request):
    orders = Order.objects.all()
    
    return render(request, 'pages/orders.html', {'orders': orders})


@login_required(login_url='admin-login-oAuth')
def delete_order(request, pk):
    order = Order.objects.get(order_id=pk)
    order.delete()
    return redirect('d-orders')


@login_required(login_url='admin-login-oAuth')
def charts(request):
    products = Product.objects.all().order_by('-id')[:12] # get the last 5 products
    nlp_reviews = NLPReviewStored.objects.all().order_by('-id')
    print(nlp_reviews.count())
    context = {
        'products': products,
        'nlp_reviews': nlp_reviews,
    }
    return render(request, 'pages/charts.html', context)


@login_required(login_url='admin-login-oAuth')
def tables(request):
    return render(request, 'pages/tables.html')


@login_required(login_url='admin-login-oAuth')
def admin_logout(request):
    logout(request)
    return redirect('admin-login-oAuth')


@login_required(login_url='admin-login-oAuth')
def user_profile(request, pk):
    user = get_object_or_404(User, id=pk)
    orders = Order.objects.filter(user=user)
    order_count = orders.count()

    # admin send message to user
    if request.method == 'POST':
        message = request.POST['message']
        sender = request.user # admin sending the message
        receiver = user # user to receive the message
        send_message = Message.objects.create(sender=sender, receiver=receiver, message=message, is_read=False)
        send_message.save()
        messages.success(request, 'Message sent successfully')
        return redirect('d-user-profile', pk=pk)
        
    context = {
        'user': user,
        'orders': orders,
        'order_count': order_count,
    }
    
    return render(request, 'pages/user_profile.html', context)

@require_GET
@login_required(login_url='admin-login-oAuth')
def search_for_user(request):
    users = User.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    return render(request, 'pages/search.html', {'users': users})


def error401(request):
    return render(request, 'errors/401.html')

def error404(request):
    return render(request, 'errors/404.html')

def error500(request):
    return render(request, 'errors/500.html')
