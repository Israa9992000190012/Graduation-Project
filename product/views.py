from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.db.models import Q
from review_blog.models import Review

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Search autocomplete
from django.views.decorators.http import require_GET

from django.contrib import messages
import math



# Caching the products to improve the performance
def get_products():
    products = cache.get('products')
    if not products:
        products = Product.objects.all()
        cache.set('products', products)
    return products


def products(request):
    products = get_products()
    product_count = products.count()
    # Pagination
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'products/products.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk) # type: ignore
    reviews_list = Review.objects.filter(product=product)

    # get the average rate for the product
    if len(reviews_list) > 0:
        total_rate = 0
        for review in reviews_list:
            total_rate += review.rating
        average_rate = math.ceil(total_rate / len(reviews_list))
    else:
        average_rate = 0

    # get all the related products based-on the category
    related_products = Product.objects.filter(product_cat=product.product_cat).exclude(id=product.id)[:15] # type: ignore
    context = {
        'product': product, 
        'related_products': related_products,
        'reviews_list': reviews_list,
        'average_rate': average_rate,
    }

    return render(request, 'products/product.html', context)


@require_GET
def search_results(request):
    query = None
    products = Product.objects.all()
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            products = products.filter(
                Q(product_name__icontains=query) |
                Q(product_price__icontains=query) |
                Q(product_cat__icontains=query)
            ).distinct() # to remove duplicate results
            
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)

import re
from time import sleep
@login_required(login_url='login')
def add_rate_for_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            rate = request.POST.get('rating')
            # check if the rate is a number
            if not re.match(r'^[0-9]+$', rate): 
                messages.error(request, 'The rate must be a number')
                sleep(2) # to prevent the user from spamming the button
                return redirect('product-details', pk=product.id) # type: ignore
            # check if the rate is between 0 and 5
            if int(rate) < 0 or int(rate) > 5:
                messages.error(request, 'The rate must be between 0 and 5')
                sleep(2) # to prevent the user from spamming the button
                return redirect('product-details', pk=product.id) # type: ignore
            # add the rate to the product
            product.rate = rate
            product.save()
            messages.success(request, 'The rate has been added successfully')
            sleep(2) # to prevent the user from spamming the button
            return redirect('product-details', pk=product.id) # type: ignore
    else:
        messages.error(request, 'You must be logged in to add a rate')
        sleep(2)
        return redirect('product-details', pk=product.id) # type: ignore
    
    return render(request, 'products/product.html', {'product': product})



import pickle

def open_pickle_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def recommend_products(request):
    products = Product.objects.all()
    # load the model of recommendation
    try:
        model = open_pickle_file('C:/Users/AHMED/Desktop/Recoomedation system/saved_model.pkl')
    except:
        print('Can not load the model')
    

    if request.method == 'POST':
        product_disc = request.POST.get('product_disc')
        # send the product description to the model
        try:
            # the model has function called show_recommendations(product_description)
            # and it will return the recommended products
            recommended_products = model.show_recommendations(product_disc)
            
        except Exception as e:
            print(e)

        # get the recommended products from the database
        #recommended_products = Product.objects.filter(product_name__in=recommended_products)
        context = {
            'recommended_products': recommended_products,
            'products': products,
        }

        return render(request, 'products/recommend_products.html', context)
    return render(request, 'products/recommend_products.html', {'products': products})
        


