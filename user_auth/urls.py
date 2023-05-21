from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('user-profile/img-edit/', views.edit_profile_pic, name='user-profile-edit-image'),
    path('user-profile/personal-info-edit/', views.update_profile_info, name='update-profile-info'),
    
    # ----------------- Inbox -----------------
    path('inbox/messages/', views.inbox_messages, name='inbox'),
    path('inbox/messages/<int:pk>/reply/', views.replyOnMessage, name='reply-on-message'),
]