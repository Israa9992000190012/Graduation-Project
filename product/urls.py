from django.urls import path
from . import views

urlpatterns = [
    path('all-products/', views.products, name='products'),
    path('product/<str:pk>/', views.product, name='product-details'),
    path('search-results/count/', views.search_results, name='search-results'),
    path('product/<str:pk>/add-rate/', views.add_rate_for_product, name='add-rate'),
    path('product/recommends/', views.recommend_products, name='recommend-products'),
]

