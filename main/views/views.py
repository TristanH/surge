from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

from main.models import Order, Item


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
    all_orders = Order.objects.filter(
        was_successful=None,
        bidding_end_time__gt=datetime.now(),
    )

    all_items = Item.objects.filter(restaurant_id=restaurant.id)

    matching_orders = []

    for order in all_orders:
        for item in all_items:
            matched_item = True
            for kw in order.keywords.tags.all():
                if not item.keywords.tags.filter(string=kw.string).exists():
                    matched_item = False
                    break

            if matched_item:
                matching_orders.append({
                    'order': order,
                    'item': item,
                })
                break

    return matching_orders


def restaurant_profile(request, restaurant_id):
    return render(request, 'index.html')