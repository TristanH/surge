import json 

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from requests import post
from requests_oauth2 import OAuth2
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta

from main.models import Order, Restuarant, Bid, Keyword, Item
from serializers import OrderSerializer, ItemSerializer, KeywordGroupSerializer, BidSerializer, KeywordSerializer

from views import get_bidding_orders, get_acc_orders


@api_view(['POST'])
@permission_classes((AllowAny,))
def call_uber(request):
    try:
        session_token = "qvf2qjSKUccNPRJKvXMHljPrz4Nvf_55SjAvKMwl"
        session = Session(server_token=session_token)
        client = UberRidesClient(session, sandbox_mode=True)
    except Exception as e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)

    # Get a ride
    try:
        response = client.get_products(request.POST['slat'], request.POST['slng'])
        products = response.json.get('products')
        product_id = products[0].get('product_id')
    except Exception as e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(id=request.POST['order_id'])
    order.delivery_time = timezone.now() + timedelta(minutes=4)
    order.save()

    # Order the ride
    try:
        import pdb; pdb.set_trace()
        response = client.request_ride(product_id=product_id,
                                   start_latitude=float(request.POST['slat']),
                                   end_latitude=float(request.POST['elat']),
                                   start_longitude=float(request.POST['slng']),
                                   end_longitude=float(request.POST['elng']))
    except Exception as e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def user_orders(request, pk):
    user = User.objects.get(username=request.GET['username'])
    hungry = HungryUser.objects.get(user=user)
    serializer = OrderSerializer(Orders.filter(hungry_user=hungry, many=True))
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_orders(request, pk):
    try:
        restauraunt = Restuarant.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    orders = get_bidding_orders(restauraunt)
    import json
    new_orders = []
    for dict_i in orders:
        new_orders.append({"order" : OrderSerializer(dict_i["order"], context={'request': request}).data,
                           "item"  : ItemSerializer(dict_i["item"], context={'request': request}).data,
                           "min_bid"  : BidSerializer(dict_i["min_bid"], context={'request': request}).data})
    orders_json = json.dumps(new_orders)
    return Response(orders_json, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_accepted_orders(request, pk):
    try:
        restauraunt = Restuarant.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    orders = get_acc_orders(restauraunt)
    import json
    new_orders = []
    for dict_i in orders:
        new_orders.append({"order" : OrderSerializer(dict_i["order"], context={'request': request}).data,
                           "item"  : ItemSerializer(dict_i["item"], context={'request': request}).data,
                           "min_bid"  : BidSerializer(dict_i["min_bid"], context={'request': request}).data})
    orders_json = json.dumps(new_orders)
    return Response(orders_json, status=status.HTTP_200_OK)


@api_view(['PUT', 'GET'])
@permission_classes((AllowAny,))
def new_order(request, pk):
    try:
            user = User.objects.get_or_create(username=request.PUT['username'])
            h_user = HungryUser.objects.get_or_create(user=user)
    except:
        return Response("No user.", status=status.HTTP_404_NOT_FOUND)
    try:
        group = KeywordGroup.objects.create()
        for i in json.loads(request.POST['keywords']):
            new_word = Keyword.objects.get(string=i)
            group.tags.add(new_word)
    except:
        return Response("Bad request for " + user.username, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(hungry_user=user,
                                 status=Order.IN_BIDDING,
                                 keywords=group,
                                 latitude=request.PUT['latitude'],
                                 longitude=request.PUT['longitude'])

    qs = Order.objects.filter(id=order.id)
    serializer = OrderSerializer(qs, many=True)

    Bid.make_default(order.id)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((AllowAny,))
def child_keywords(request):
    pre_kws = set(json.loads(request.POST['keywords']))
    valid_children = set()

    for item in Item.objects.all():
        wrong_item = False
        for kw_id in pre_kws:
            if not item.keywords.tags.filter(id=kw_id).exists():
                wrong_item = True

        if wrong_item:
            continue

        for kw in item.keywords.tags.exclude(id__in=pre_kws, is_main=True):
            valid_children.add(kw.id)

    ks = KeywordSerializer(Keyword.objects.filter(id__in=valid_children), many=True)
    return Response(ks.data, status=status.HTTP_200_OK)


