from django.urls import path, include
from . import views
from .views import custom_logout, buy_now, edit_account, cancel_auction
from django.conf.urls.static import static
from django.conf import settings

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
    path('accounts/', include('django.contrib.auth.urls')),
    path('auction/<int:pk>/buy/', buy_now, name='buy_now'),
    path('edit_account/', edit_account, name='edit_account'),
    path('auction/new/', views.create_auction, name='create_auction'),
    path('auction/<int:pk>/cancel/', cancel_auction, name='cancel_auction'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add-to-watchlist/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('ending-soon/', views.ending_soon_auctions, name='ending_soon_auctions'),
    path('user-auctions/', views.user_auctions, name='user_auctions'),
    path('user-bids/', views.user_bids, name='user_bids'),
    path('observed-auctions/', views.observed_auctions, name='observed_auctions'),
    path('recently-ended/', views.recently_ended_auctions, name='recently_ended_auctions'),
    path('category/<int:category_id>/', views.auction_search_by_category, name='auction_search_by_category'),
    path('search/', views.auction_search, name='auction_search'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    # Other URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
