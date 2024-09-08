from django import forms
from .models import Auction
from .models import Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'photos', 'category', 'minimum_amount', 'buy_now_amount', 'promoted',
                  'end_date']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter your bid amount'}),
        }
