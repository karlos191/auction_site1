from django.urls import path
from . import views
from .views import custom_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),
    path('auctions/', views.auctions_list, name='auctions_list'),
    path('auction/<int:pk>/', views.auction_detail, name='auction_detail'),
    path('login/', views.custom_login, name='login'),
    path('logout/', custom_logout, name='custom_logout'),
    path('place_bid/<int:pk>/', views.place_bid, name='place_bid'),
    # Other URL patterns
]

