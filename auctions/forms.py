from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Auction, Comment
from django.contrib.auth.models import User


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AuctionForm, self).__init__(*args, **kwargs)

        # Cast the user to CustomUser if it's passed
        if isinstance(user, CustomUser) and user.account_type != 'PREMIUM':
            self.fields.pop('promoted')  # Remove the promoted field for non-premium users


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your comment...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
