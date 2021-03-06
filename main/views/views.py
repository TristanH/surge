from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.db.models import Avg, Max, Min

from main.models import Order, Item, Bid


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def bidding(request):
    return render(request, 'bidding.html', {'orders': get_bidding_orders(request.user.restaurant())})

@login_required
def accepted(request):
    return render(request, 'accepted.html', {'orders': get_acc_orders(request.user.restaurant())})


def get_bidding_orders(restaurant):
    # Expiriy Time after now
    # Location nearby (hack? same city)
    # Keywords all match some meal that the restaurant has
        # Load all orders
        # Load all items
        # Only take the ones with all shared keywords
    all_orders = Order.objects.filter(
        was_successful=None,
        bidding_end_time__gt=timezone.now(),
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
                    'min_bid': get_min_bid(order.id),
                })
                break

    return matching_orders


def get_acc_orders(restaurant):
    # Expiriy Time after now
    # Location nearby (hack? same city)
    # Keywords all match some meal that the restaurant has
        # Load all orders
        # Load all items
        # Only take the ones with all shared keywords
    all_orders = Order.objects.filter(
        bidding_end_time__lt=timezone.now(),
    ).order_by("bidding_end_time")

    all_items = Item.objects.filter(restaurant_id=restaurant.id)

    matching_orders = []

    for order in all_orders:
        if order.pickup_time and order.pickup_time < timezone.now():
            continue

        try:
            bid = Bid.objects.get(won=True, order=order)
        except Exception:
            continue

        if all_items.filter(id=bid.item_id).exists():
            matching_orders.append({
                'order': order,
                'item': bid.item,
                'min_bid': bid,
            })
            break

    return matching_orders


def get_min_bid(order_id):
    min_bid = Bid.objects.filter(order_id=order_id).order_by('price')
    if min_bid.exists():
        min_bid = min_bid[0]
    else:
        min_bid = None
        # TODO: hack this if need be
    return min_bid


@login_required
def place_bid(request):
    order_id = request.GET.get('order')
    item_id = request.GET.get('item')
    amount = int(request.GET.get('bid'))
    restaurant = request.user.restaurant()

    existing_bid = get_min_bid(order_id)

    if amount < existing_bid.price:
        existing_bid.won=False
        existing_bid.save()
        new_bid = Bid(item_id=item_id, order_id=order_id, won=True, price=amount)
        new_bid.save()
    else:
        return HttpResponse("You ordered too late!")

    return redirect('bidding')

@login_required
def restaurant_profile(request):
    return render(request, 'restaurant_profile.html', {
        'items': Item.objects.filter(restaurant_id=request.user.restaurant().id)
    })