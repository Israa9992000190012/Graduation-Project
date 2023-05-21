from django.shortcuts import render
from review_blog.decorators import unauthenticated_user, allowed_users, admin_only


def index(request):
    return render(request, 'base/main.html')

def about(request):
    return render(request, 'base/about.html')

def delivery(request):
    return render(request, 'base/delivery.html')

def contact(request):   
    return render(request, 'base/contactUs.html')