from django.db import models
from django.contrib.auth.models import User


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='category_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    account_status = models.CharField(max_length=10,
                                      choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('BLOCKED', 'Blocked')])
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=[('NORMAL', 'Normal'), ('PREMIUM', 'Premium')])

    def __str__(self):
        return self.user.username


# Auction Model
class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to='auction_photos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promoted = models.BooleanField(default=False)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    num_visits = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buy_now_price = None

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bid {self.amount} on {self.auction}'
