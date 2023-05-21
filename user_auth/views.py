from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from adminside.models import Message, ReplyOnMessage

from .models import Profile
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from payment.models import Order


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name='Not set', last_name='Not set')
                    # Create profile for each user when they register
                    Profile.objects.create(user=user)
                    # Add user to customer group
                    group = Group.objects.get(name='customer')
                    user.groups.add(group)
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'auth/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'auth/login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')   


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    for order in orders:
        if order.status == 'Pending':
            order.status = 'Delivered'
            order.save()
    
    context = {
        'orders': orders,
        'user': user,
    }
    return render(request, 'auth/profile.html', context)

@login_required(login_url='login')
def inbox_messages(request):
    user = request.user
    user_messages = Message.objects.filter(receiver=user)
    context = {
        'user_messages': user_messages,
    }
    return render(request, 'auth/inbox.html', context)

@login_required(login_url='login')
def replyOnMessage(request, pk):
    if request.method == 'POST':
        msg = get_object_or_404(Message, id=pk)
        reply = request.POST['reply']
        sender = request.user 
        receiver = msg.sender
        
        ReplyOnMessage.objects.create(msg=msg, sender=sender, receiver=receiver, reply=reply)
        messages.success(request, 'Reply sent')
        return redirect('inbox')
    else:
        return redirect('inbox')

@login_required(login_url='login')
def edit_profile_pic(request):
    if request.method == 'POST':
        try:
            img = request.FILES['profile_pic_']
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.profile_pic = img
            profile.save()
            messages.success(request, 'Profile picture updated')
            return redirect('user-profile')
        except Exception as e:
            messages.error(request, 'Something went wrong on our end. Please try again later.')
            return redirect('user-profile')

    return render(request, 'auth/profile.html')


@login_required(login_url='login')
def update_profile_info(request):
    if request.method == 'POST':
        try:
            user = request.user
            profile = get_object_or_404(Profile, user=user)
            profile.first_name = request.POST['first_name']
            profile.last_name = request.POST['last_name']
            profile.email = request.POST['email']
            profile.phone = request.POST['phone']
            profile.city = request.POST['city']
            profile.state = request.POST['state']
            profile.zipcode = request.POST['zipcode'] 
            profile.country = request.POST['country']
            profile.save()

            # Update user info on User model also
            User.objects.filter(id=user.id).update(first_name=profile.first_name, last_name=profile.last_name, email=profile.email)
            
            messages.success(request, 'Profile information updated')
            return redirect('user-profile')
       
        except Exception as e:
            messages.error(request, 'Something went wrong on our end. Please try again later.')
            return redirect('user-profile')

    return render(request, 'auth/profile.html')

