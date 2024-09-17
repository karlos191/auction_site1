from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, CustomUser, Auction, Bid


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
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'city', 'address', 'profile_image', 'account_status', 'account_type')}),
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
    list_display = ('title', 'starting_price', 'current_price', 'minimum_amount', 'start_date', 'end_date')
    search_fields = ('title', 'starting_price', 'current_price', 'start_date', 'end_date')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('user__username', 'auction__title')
