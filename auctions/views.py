from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BidForm
from .forms import CustomUserCreationForm
from .models import Auction, Bid
from django.utils import timezone


def home(request):
    recent_auctions = Auction.objects.all().order_by('-start_date')[:10]
    return render(request, 'auctions/home.html', {'recent_auctions': recent_auctions})


def auctions_list(request):
    auctions = Auction.objects.all()
    return render(request, 'auctions/auctions_list.html', {'auctions': auctions})


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    form = BidForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > auction.current_price:
            Bid.objects.create(auction=auction, user=request.user, amount=amount)
            auction.current_price = amount
            auction.save()
            messages.success(request, 'Bid placed successfully!')
        else:
            messages.error(request, 'Bid amount must be higher than the current price.')
        return redirect('auction_detail', pk=pk)

    return render(request, 'auctions/auction_detail.html', {'auction': auction, 'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or another page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def custom_logout(request):
    if request.method == 'POST':  # Ensures it's a POST request
        logout(request)
        return redirect('home')  # Redirect to home or another page after logout
    else:
        return redirect('home')  # Redirect if it's not a POST request


@login_required
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    # Check if the auction has ended
    if auction.end_date < timezone.now() or auction.is_closed:
        messages.error(request, "This auction has already ended. You cannot place a bid.")
        return redirect('auction_detail', pk=pk)

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Check if the bid amount is higher than the current price
            if amount > auction.current_price:
                Bid.objects.create(auction=auction, user=request.user, amount=amount)
                auction.current_price = amount
                auction.save()
                messages.success(request, 'Bid placed successfully!')
                return redirect('auction_detail', pk=pk)
            else:
                messages.error(request, 'Bid amount must be higher than the current price.')
    else:
        form = BidForm()

    return render(request, 'auctions/place_bid.html', {'auction': auction, 'form': form})


def profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})


@login_required
def buy_now(request, pk):
    # Get the auction object; if it doesn't exist, return a 404 error.
    auction = get_object_or_404(Auction, pk=pk)

    # Check if the auction is already ended or if there's no buy now price.
    if auction.end_date < timezone.now():
        messages.error(request, "This auction has already ended.")
        return redirect('auction_detail', pk=pk)

    if auction.buy_now_price is None:
        messages.error(request, "This auction does not have a 'Buy Now' price.")
        return redirect('auction_detail', pk=pk)

    # Ensure the user is not trying to buy their own auction
    if auction.user == request.user:
        messages.error(request, "You cannot buy your own auction.")
        return redirect('auction_detail', pk=pk)

    # Create a new Bid for the Buy Now action
    # You can customize this part depending on how you want to handle the purchase
    try:
        # Optionally, you can create a bid record to track the buy now transaction.
        Bid.objects.create(auction=auction, user=request.user, amount=auction.buy_now_price)

        # Optionally, mark the auction as sold or inactive (add a sold field in the Auction model if needed)
        auction.current_price = auction.buy_now_price
        auction.save()

        messages.success(request, f"You have successfully bought '{auction.title}' for ${auction.buy_now_price}!")
        return redirect('auction_detail', pk=pk)
    except Exception as e:
        messages.error(request, f"An error occurred while processing your purchase: {str(e)}")
        return redirect('auction_detail', pk=pk)