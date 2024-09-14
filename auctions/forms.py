from django import forms
from .models import Auction
from .models import Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'photos', 'category', 'minimum_amount', 'buy_now_amount', 'promoted',
                  'end_date']


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Bid Amount',
        help_text='Enter your bid amount.'
    )
