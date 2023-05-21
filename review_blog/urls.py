from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blogs, name='blogs'),
    path('reviews/<int:pk>/', views.reviews, name='product-reviews'),
    path('blog/<int:pk>/', views.blog, name='blog-details'),
    path('blog/create/', views.create_blog, name='create-blog'),
    path('add-review/<int:pk>/', views.add_review, name='add-review'),
    path('delete-review/<int:pk>/', views.delete_review, name='delete-review'),
    path('add-comment-on-blog/<int:pk>/', views.comment_on_blog, name='add-comment-on-blog'),
]