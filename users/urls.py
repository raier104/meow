from django.urls import path
from . import views

app_name = 'users'  # Add this line if you use namespace='users' in your main urls.py

urlpatterns = [
    path('', views.user_home_page, name='user_home_page'),    
    path('login/', views.user_login, name='login'),     
    path('logout/', views.logout_view, name='logout'),
    path('contact_us/', views.contact_us_view, name='contact_us'),  
    path('register/', views.user_register, name='register'), #URL pattern for profile
    path('profile/', views.profile, name='profile'),  # <-- Add this line
]

