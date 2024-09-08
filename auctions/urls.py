from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),
    path('auctions/', views.auctions_list, name='auctions_list'),
    path('auction/<int:pk>/', views.auction_detail, name='auction_detail'),
    path('login/', views.custom_login, name='login'),  # Use view function for login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use built-in logout view
    path('place_bid/<int:pk>/', views.place_bid, name='place_bid'),
    # Other URL patterns
]

