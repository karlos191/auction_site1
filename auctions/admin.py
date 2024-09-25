from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, CustomUser, Auction, Bid
from django.utils import timezone
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to be displayed in the admin list view
    list_display = ['username', 'email', 'city', 'address', 'account_status', 'account_type', 'date_joined']

    # Fields to be used in the edit form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('city', 'address', 'profile_image', 'account_status', 'account_type')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    # Fields to be used in the creation form
    add_fieldsets = (
        (None, {'fields': (
            'username', 'email', 'password1', 'password2', 'city', 'address', 'profile_image', 'account_status',
            'account_type')}),
    )

    # Specify which fields are readonly
    readonly_fields = ['date_joined']

    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Customize as needed


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'starting_price', 'description', 'current_price', 'buy_now_price', 'minimum_amount', 'start_date',
        'end_date')
    search_fields = (
        'title', 'description', 'user', 'minimum_amount', 'starting_price', 'current_price', 'start_date', 'end_date')
    exclude = ('start_date', 'user')
    fieldsets = (
        (None, {'fields': (
            'title', 'category', 'description', 'minimum_amount', 'starting_price', 'current_price', 'buy_now_price', 'end_date')}),
    )
    readonly_fields = ('start_date',)  # Make start_date read-only

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if the auction is being created
            obj.start_date = timezone.now()  # Automatically set start_date
            obj.user = request.user  # Automatically assign current logged-in user to auction
        super().save_model(request, obj, form, change)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('user__username', 'auction__title')
