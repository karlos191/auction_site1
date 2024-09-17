from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.conf import settings


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
