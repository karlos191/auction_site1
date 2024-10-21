from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Auction, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'city', 'address', 'profile_image', 'account_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "User name (presented on the account profile)"
        self.fields['email'].label = "Login (email used for communication and notifications)"
        self.fields['city'].label = "City"
        self.fields['address'].label = "Address (street, house number, ZIP code)"
        self.fields['profile_image'].label = "Logotype / thumbnail / avatar"
        self.fields['account_type'].label = "Type (NORMAL / PREMIUM)"


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Bid Amount',
        help_text='Enter your bid amount.'
    )


class EditAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'city', 'profile_image']

    def save(self, commit=True):
        user = super().save(commit)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'photos', 'category', 'starting_price', 'buy_now_price', 'minimum_amount',
                  'end_date', 'promoted']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_starting_price(self):
        starting_price = self.cleaned_data.get('starting_price')
        if starting_price is not None and starting_price < 0:
            raise ValidationError("The starting price cannot be negative.")
        return starting_price

    def clean_minimum_amount(self):
        minimum_amount = self.cleaned_data.get('minimum_amount')
        if minimum_amount is not None and minimum_amount < 0:
            raise ValidationError("The minimum amount cannot be negative.")
        return minimum_amount

    def clean_buy_now_price(self):
        buy_now_price = self.cleaned_data.get('buy_now_price')
        if buy_now_price is not None and buy_now_price < 0:
            raise ValidationError("The buy-now price cannot be negative.")
        return buy_now_price

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date < timezone.now():
            raise ValidationError("The end date cannot be in the past.")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        starting_price = cleaned_data.get("starting_price")
        buy_now_price = cleaned_data.get("buy_now_price")

        if buy_now_price and starting_price and buy_now_price <= starting_price:
            self.add_error('buy_now_price', "The buy-now price must be higher than the starting price.")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AuctionForm, self).__init__(*args, **kwargs)

        if isinstance(user, CustomUser) and user.account_type != 'PREMIUM':
            self.fields.pop('promoted')  # Remove the promoted field for non-premium users


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'rows': 4,
                'cols': 40,
            }),
            'rating': forms.NumberInput(attrs={
                'min': 0,
                'max': 5,
                'step': 1,
                'placeholder': 'Rate 1-5'
            }),
        }
