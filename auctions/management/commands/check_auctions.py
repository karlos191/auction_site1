from django.core.management.base import BaseCommand
from django.utils import timezone
from auctions.models import Auction, Bid
from django.db.models import Max


class Command(BaseCommand):
    help = 'Checks and updates auction statuses periodically'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        # Get all active auctions that have passed their end date
        active_auctions = Auction.objects.filter(is_closed=False, end_date__lt=now)

        for auction in active_auctions:
            # Get the highest bid for the auction
            highest_bid = Bid.objects.filter(auction=auction).aggregate(Max('amount'))['amount__max']

            if highest_bid and highest_bid >= auction.minimum_amount:
                # Notify the highest bidder
                highest_bid_instance = Bid.objects.filter(auction=auction, amount=highest_bid).first()
                auction.winner = highest_bid_instance.user
                auction.is_closed = True
                auction.save()

                # Here, you can send a message or email to the user about winning the auction
                self.stdout.write(
                    self.style.SUCCESS(f"Auction {auction.title} has been won by {highest_bid_instance.user.email}"))
            else:
                # Auction didn't meet minimum price, close without a winner
                auction.is_closed = True
                auction.save()

                self.stdout.write(self.style.WARNING(f"Auction {auction.title} closed without a winner"))

        self.stdout.write(self.style.SUCCESS("Auction check completed."))
