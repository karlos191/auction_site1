from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BidForm
from .forms import CustomUserCreationForm
from .models import Auction, Bid, Category, CustomUser, Comment
from django.utils import timezone
from .forms import EditAccountForm
from .forms import AuctionForm, CommentForm
from django.db.models import Count
from django.db import models

User = get_user_model()


def home(request):
    # Current time
    now = timezone.now()

    # Recent auctions
    recent_auctions = Auction.objects.filter(is_canceled=False).order_by('-start_date')[:10]

    # Categories
    categories = Category.objects.all()

    won_auctions = Auction.objects.none()

    # Initialize empty lists for unauthenticated users
    user_auctions = auctions_bidding = watchlist_auctions = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Auctions created by the logged-in user
        user_auctions = Auction.objects.filter(user=request.user, is_canceled=False)

        # Auctions the user is bidding on
        auctions_bidding = Auction.objects.filter(bids__user=request.user, is_canceled=False).distinct()

        # Auctions the user is watching
        watchlist_auctions = request.user.watchlist.all()

        # Fetch auctions won by the logged-in user, either by bidding or Buy Now
        won_auctions = Auction.objects.filter(winner=request.user)

    # Auctions that are ending soon (exclude closed auctions)
    ending_auctions = Auction.objects.filter(is_canceled=False, end_date__gte=now, is_closed=False).order_by(
        'end_date')[:10]

    # Just ended auctions (include closed auctions or those that ended by time)
    ended_auctions = Auction.objects.filter(is_canceled=False, is_closed=True) | Auction.objects.filter(
        end_date__lt=now).order_by('-end_date')[:10]

    # Query to get top 5 users with the most auctions
    top_users = User.objects.annotate(auction_count=Count('auctions')).order_by('-auction_count')[:5]

    return render(request, 'auctions/home.html', {
        'recent_auctions': recent_auctions,
        'categories': categories,
        'now': now,
        'user_auctions': user_auctions,
        'auctions_bidding': auctions_bidding,
        'watchlist_auctions': watchlist_auctions,
        'ending_auctions': ending_auctions,
        'ended_auctions': ended_auctions,
        'top_users': top_users,
        'won_auctions': won_auctions,
    })


def auctions_list(request):
    auctions = Auction.objects.all()
    return render(request, 'auctions/auctions_list.html', {'auctions': auctions})


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    form = BidForm(request.POST or None)
    now = timezone.now()
    auction_has_ended = auction.end_date < now
    auction.num_visits += 1
    auction.save()

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

    return render(request, 'auctions/auction_detail.html',
                  {'auction': auction, 'form': form, 'now': now, 'auction_has_ended': auction_has_ended})


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

    if auction.end_date < timezone.now() or auction.is_closed:
        messages.error(request, "This auction has already ended. You can no longer place bids.")
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
    auction = get_object_or_404(Auction, pk=pk)

    # Ensure auction hasn't ended or is already closed
    if auction.end_date < timezone.now() or auction.is_closed:
        messages.error(request, "This auction has already ended.")
        return redirect('auction_detail', pk=pk)

    if auction.buy_now_price is None:
        messages.error(request, "This auction does not have a 'Buy Now' price.")
        return redirect('auction_detail', pk=pk)

    # Prevent buyer from buying their own auction
    if auction.user == request.user:
        messages.error(request, "You cannot buy your own auction.")
        return redirect('auction_detail', pk=pk)

    try:
        # Mark auction as sold
        auction.current_price = auction.buy_now_price
        auction.winner = request.user
        auction.is_closed = True
        auction.save()

        messages.success(request, f"You have successfully bought '{auction.title}' for ${auction.buy_now_price}.")
        return redirect('auction_detail', pk=pk)

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('auction_detail', pk=pk)


@login_required
def edit_account(request):
    user = request.user

    if request.method == 'POST':
        form = EditAccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account details updated successfully.')
            return redirect('edit_account')
    else:
        form = EditAccountForm(instance=user)

    return render(request, 'auctions/edit_account.html', {'form': form})


@login_required
def create_auction(request):
    user = request.user  # Get the logged-in user

    # Cast to CustomUser to help IDE recognize the 'city' field (if using a custom user model)
    user = CustomUser.objects.get(pk=user.pk)  # This is only necessary if using a CustomUser model

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, user=user)  # Pass the user to the form
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = user  # Assign the logged-in user to the auction
            auction.location = user.city  # Assign the user's city to the auction location

            # Check if promotion is allowed based on the user's account type
            if auction.promoted and user.account_type == 'PREMIUM':
                current_month = timezone.now().month
                promoted_auctions_count = Auction.objects.filter(user=user, promoted=True,
                                                                 start_date__month=current_month).count()

                if promoted_auctions_count >= 10:
                    messages.error(request, 'You have already promoted the maximum of 10 auctions this month.')
                    return redirect('create_auction')  # Redirect them back to the auction creation form

            auction.save()  # Save the auction if everything is valid
            messages.success(request, 'Auction created successfully!')
            return redirect('auction_detail', pk=auction.pk)
        else:
            print(form.errors)  # Print form validation errors to the console for debugging
            messages.error(request, 'There was an error with your submission. Please check the form fields.')
    else:
        form = AuctionForm(user=user)  # Pass the user to the form

    return render(request, 'auctions/create_auction.html', {'form': form})


@login_required
def cancel_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    # Check if the auction has any bids or if it's already closed
    if auction.bids.exists() or auction.is_closed:
        messages.error(request, "This auction cannot be canceled as it has bids or is already closed.")
        return redirect('auction_detail', pk=pk)

    # Mark the auction as canceled
    auction.is_canceled = True
    auction.is_closed = True  # Also mark it as closed so it doesn't appear as active
    auction.save()

    messages.success(request, "Auction canceled successfully.")
    return redirect('home')


@login_required
def add_to_watchlist(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if auction in request.user.watchlist.all():
        messages.info(request, "You are already watching this auction.")
    else:
        request.user.watchlist.add(auction)
        messages.success(request, "Auction added to your watchlist.")
    return redirect('auction_detail', pk=pk)


@login_required
def remove_from_watchlist(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if auction in request.user.watchlist.all():
        request.user.watchlist.remove(auction)
        messages.success(request, "Auction removed from your watchlist.")
    else:
        messages.info(request, "This auction is not in your watchlist.")
    return redirect('auction_detail', pk=pk)


@login_required
def watchlist(request):
    watched_auctions = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watched_auctions': watched_auctions})


def ending_soon_auctions(request):
    ending_auctions = Auction.objects.filter(end_date__gt=timezone.now()).order_by('end_date')[:10]
    return render(request, 'auctions/ending_auctions.html', {'ending_auctions': ending_auctions})


@login_required
def user_auctions(request):
    user_auctions = Auction.objects.filter(user=request.user)
    return render(request, 'auctions/user_auctions.html', {'user_auctions': user_auctions})


@login_required
def user_bids(request):
    user_bids = Auction.objects.filter(bids__user=request.user).distinct()
    return render(request, 'auctions/user_bids.html', {'user_bids': user_bids})


@login_required
def observed_auctions(request):
    observed_auctions = request.user.watchlist.all()
    return render(request, 'auctions/observed_auctions.html', {'observed_auctions': observed_auctions})


def recently_ended_auctions(request):
    recently_ended_auctions = Auction.objects.filter(end_date__lte=timezone.now()).order_by('-end_date')[:10]
    return render(request, 'auctions/recently_ended_auctions.html',
                  {'recently_ended_auctions': recently_ended_auctions})


def auction_search_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    auctions = Auction.objects.filter(category=category, is_closed=False)

    context = {
        'category': category,
        'auctions': auctions,
    }
    return render(request, 'auctions/auction_search_results.html', context)


def auction_search(request):
    query = request.GET.get('query', '')
    search_results = Auction.objects.filter(title__icontains=query, is_closed=False) if query else []

    context = {
        'search_results': search_results,
        'query': query,
    }
    return render(request, 'auctions/auction_search.html', context)


@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(CustomUser, pk=user_id)
    comments = user_profile.comments_received.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user_profile  # User being commented on
            comment.commenter = request.user  # User leaving the comment
            comment.save()
            messages.success(request, 'Comment and rating added successfully!')
            return redirect('user_profile', user_id=user_profile.id)
    else:
        form = CommentForm()

    avg_rating = comments.aggregate(models.Avg('rating'))['rating__avg'] or 0

    return render(request, 'auctions/user_profile.html', {
        'user_profile': user_profile,
        'comments': comments,
        'form': form,
        'avg_rating': avg_rating
    })
