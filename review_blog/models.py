from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from product.models import Product
from user_auth.models import Profile

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    blog_image = models.ImageField(upload_to='blog_images', blank=True, null=True, default='blog_pics/blog.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:30]

    def get_absolute_url(self):  # its a method that returns the url to a particular instance of a model
        return reverse('blog-details', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
    


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=300)
    review = models.TextField()
    rating = models.IntegerField(default=0)
    has_rated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name # type: ignore
    
    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) # to get user profile picture
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:30]
    
    class Meta:
        ordering = ['-created_at']


class NLPReviewStored(models.Model):
    review = models.CharField(max_length=800)
    sentiment = models.CharField(max_length=300)

    def __str__(self):
        return self.sentiment
    
    class Meta:
        ordering = ['-review']