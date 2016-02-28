from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from requests import post
from requests_oauth2 import OAuth2
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

from django.contrib.auth.models import User   

from main.models import Order, Restuarant, Bid
from serializers import OrderSerializer, ItemSerializer, KeywordGroupSerializer, BidSerializer

from views import get_bidding_orders


@api_view(['POST'])
@permission_classes((AllowAny,))
def call_uber(request):
    try:
        session_token = "qvf2qjSKUccNPRJKvXMHljPrz4Nvf_55SjAvKMwl"
        session = Session(server_token=session_token)
        client = UberRidesClient(session, sandbox_mode=True)
    except e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)

    # Get a ride
    try:
        response = client.get_products(request.POST['slat'], request.POST['slng'])
        products = response.json.get('products')
        product_id = products[0].get('product_id')
    except e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)

    # Order the ride
    try:
        response = client.request_ride(product_id=product_id,
                                   start_latitude=request.POST['slat'],
                                   end_latitude=request.POST['elat'],
                                   start_longitude=request.POST['slng'],
                                   end_longitude=request.POST['elng'])
    except e:
        return Response(e.info, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)

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


@api_view(['PUT'])
@permission_classes((AllowAny,))
def new_keyword(request, pk):
    try:
        user = User.objects.all()[0]
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:    
        group = KeywordGroup.objects.create(tags=request.POST['keywords'])
    except:
        return Response("Bad request for " + user, sttus=status.HTTP_400_BAD_REQUEST)
    qs = KeywordGroup.objects.filter(id=group.id)
    serializer = KeywordGroupSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes((AllowAny,))
def new_order(request, pk):
    # TODO make a dummy user
    # TODO test
    try:
        user = User.objects.all()[0]
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        order = Order.objects.create(hungry_user=user,
                                 status=Order.IN_BIDDING,
                                 keywords=request.PUT['keywords'],
                                 latitude=request.PUT['latitude'],
                                 longitude=request.PUT['longitude'])
    except:
        return Response("Bad request for " + user, status=status.HTTP_400_BAD_REQUEST)

    qs = Order.objects.filter(id=order.id)
    serializer = OrderSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

