from django.contrib import admin
from .models import Category, UserProfile
from .models import Auction, Bid

# Register models in the Django admin
admin.site.register(Category)
admin.site.register(UserProfile)


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'minimum_amount', 'end_date')  # Customize as needed
    search_fields = ('title',)  # Add fields to search


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('user__username', 'auction__title')
