from .models import Blog, Review, Comment, NLPReviewStored
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from product.models import Product


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from .load_ml import load_model, load_vectorizer


def blogs(request):
    # get all blogs from database
    blogs = Blog.objects.all().order_by('-created_at')
    # get the number of blogs
    blog_count = blogs.count()
    # paginate blogs
    page = request.GET.get('page', 1) # get the page number
    paginator = Paginator(blogs, 3) # show 3 blogs per page
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage: # if page is out of range
        blogs = paginator.page(paginator.num_pages)


    context = {
        'blogs': blogs,
        'blog_count': blog_count,
    }
    return render(request, 'reviews/blog.html', context)


def blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        'blog': blog,
    }
    return render(request, 'reviews/blog_details.html', context)


@login_required(login_url='login')
def comment_on_blog(request, pk):
    
    try:
        blog = get_object_or_404(Blog, pk=pk)
        user_profile = request.user.profile
        
    except:
        blog = get_object_or_404(Blog, pk=pk)
        user_profile = None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        # create comment
        Comment.objects.create(user=request.user, comment=comment, blog=blog, user_profile=user_profile)
        messages.success(request, 'Comment added successfully!')
        return redirect('blog-details', pk=blog.pk)

    else:
        messages.error(request, 'Error adding comment!')
        return redirect('blog-details', pk=blog.pk)


def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully!')
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/add_blog.html', context)



# create view for getting all reviews for a particular product
def reviews(request, pk):
    # 1- get the product and user who posted the review
    try:
        product = get_object_or_404(Product, pk=pk)
    except:
        messages.error(request, 'Product not found!')
        return redirect('home')

    print(f'product: {product}')
    # 2- get all reviews for the product
    reviews = Review.objects.filter(product=product) # type: ignore

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'reviews/reviews.html', context)


def add_review(request, pk):
    # 1- get the product
    product = get_object_or_404(Product, pk=pk) # type: ignore
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        # take the review and pass it to the ML model
        # load the vectorizer
        vectorizer = load_vectorizer()
        # load the model
        model = load_model()
        # vectorize the review
        review_vector = vectorizer.transform([review])
        # predict the sentiment
        prediction = model.predict(review_vector)
        # get the sentiment
        sentiment = prediction[0]

        print(f'sentiment: {sentiment} , rating: {rating}')

        try:
            # create NLPReviewStored object
            NLPReviewStored.objects.create(review=review, sentiment=sentiment) # type: ignore
        except:
            print('Error creating NLPReviewStored object!')

        # create review
        has_rated = Review.objects.filter(user=user, product=product).exists() # type: ignore
        if has_rated:
            messages.error(request, 'You have already reviewed this product!')
            return redirect('product-details', pk=product.pk)
        else:  
            Review.objects.create(user=user, name=name, review=review, rating=rating, product=product) # type: ignore
            messages.success(request, 'Review added successfully!')
            return redirect('product-details', pk=product.pk)

    else:
        messages.error(request, 'Error adding review!')
        return redirect('product-details', pk=product.pk)


def delete_review(request, pk):
    # 1- get the review
    review = get_object_or_404(Review, pk=pk)
    # 2- get the product
    product = review.product
    # 3- delete the review
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('product-details', pk=product.pk)

