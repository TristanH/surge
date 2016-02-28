from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User   

from main.models import Order, Restuarant
from serializers import OrderSerializer, ItemSerializer, BidSerializer

from views import get_bidding_orders


@api_view(['POST'])
@permission_classes((AllowAny,))
def call_lyft(request):
    return Response(status=HTTP_404_NOT_FOUND)


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

