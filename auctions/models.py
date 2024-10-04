from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='category_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auctions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to='auction_photos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, )
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promoted = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now, editable=False)
    end_date = models.DateTimeField()
    num_visits = models.IntegerField(default=0)
    is_canceled = models.BooleanField(default=False)
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watching_auctions', blank=True)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='won_auctions')

    def check_if_winner(self):
        # Check if the auction has ended by date
        if self.end_date <= timezone.now() and not self.is_closed:
            highest_bid = self.bids.order_by('-amount').first()
            # Check if the highest bid is greater than or equal to the minimum amount
            if highest_bid and highest_bid.amount >= self.minimum_amount:
                self.winner = highest_bid.user  # Mark the highest bidder as the winner
                self.is_closed = True
                self.save()
            else:
                # Auction ends without a winner
                self.is_closed = True
                self.save()

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    watchlist = models.ManyToManyField('Auction', related_name='watched_by', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    account_status = models.CharField(
        max_length=10, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('BLOCKED', 'Blocked')]
    )
    account_type = models.CharField(
        max_length=10, choices=[('NORMAL', 'Normal'), ('PREMIUM', 'Premium')]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bid {self.amount} on {self.auction}'


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='comments_received', on_delete=models.CASCADE
    )
    commenter = models.ForeignKey(
        CustomUser, related_name='comments_made', on_delete=models.SET_NULL, null=True
    )
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username if self.commenter else 'Anonymous'} on {self.user.username}"
