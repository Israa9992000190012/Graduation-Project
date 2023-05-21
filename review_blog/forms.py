from django import forms
from .models import Blog, Review

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'review']