from django.shortcuts import render
from django.http import HttpResponse

from main.models import Order


# Create your views here.
def index(request):
    return render(request, 'index.html')


def bidding(request):
    return render(request, 'bidding.html', {'orders': get_bidding_orders(request.user.restaurant())})


def get_bidding_orders(restaurant):
    # Expiriy Time after now
    # Location nearby (hack? same city)
    # Keywords all match some meal that the restaurant has
        # Load all orders
        # Load all items
        # Only take the ones with all shared keywords
    return Order.objects.all()


def restaurant_profile(request):
    return render(request, 'index.html')