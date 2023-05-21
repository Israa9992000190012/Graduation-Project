from django.urls import path
from . import views

urlpatterns = [
    path('admin-register-oAuth/', views.admin_register, name='admin-register-oAuth'),
    path('admin-login-oAuth/', views.admin_login, name='admin-login-oAuth'),
    path('admin-logout-oAuth/', views.admin_logout, name='admin-logout-oAuth'),
    path('', views.index, name='d-index'),
    path('products/', views.products, name='d-products'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
    path('update-product/<int:pk>/', views.update_product, name='update-product'),

    path('orders/', views.orders, name='d-orders'),
    path('delete-order/<str:pk>/', views.delete_order, name='delete-order'),


    path('charts/', views.charts, name='d-charts'),
    path('tables/', views.tables, name='d-tables'),
    path('user-profile/<int:pk>/', views.user_profile, name='d-user-profile'),
    


    # charts
    



    
    path('error/401-error/', views.error401, name='error401'),
    path('error/404-error/', views.error404, name='error404'),
    path('error/500-error/', views.error500, name='error500'),
]