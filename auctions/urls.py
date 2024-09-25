from django.urls import path, include
from . import views
from .views import custom_logout, buy_now, edit_account

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),
    path('auctions/', views.auctions_list, name='auctions_list'),
    path('auction/<int:pk>/', views.auction_detail, name='auction_detail'),
    path('login/', views.custom_login, name='login'),
    path('logout/', custom_logout, name='custom_logout'),
    path('place_bid/<int:pk>/', views.place_bid, name='place_bid'),
    path('profile/', views.profile, name='profile'),
    path('buy_now/<int:pk>/', buy_now, name='buy_now'),
    path('accounts/', include('django.contrib.auth.urls')),  # This will include login/logout views
    path('auction/<int:pk>/buy/', buy_now, name='buy_now'),
    path('edit_account/', edit_account, name='edit_account'),
    # Other URL patterns
]
