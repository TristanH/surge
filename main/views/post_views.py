from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User   

from main.models import Order
from serializers import OrderSerializer

@api_view(['PUT'])
@permission_classes((AllowAny,))
def new_order(request, pk):
    # TODO test
    try:
        user = User.objects.get(pk=pk)
        order = Order.objects.create(hungry_user=user,
                                 status=Order.IN_BIDDING,
                                 keywords=request.PUT['keywords'],
                                 latitude=request.PUT['latitude'],
                                 longitude=request.PUT['longitude'])
    except:
        return Response("Bad request.", status=status.HTTP_400_BAD_REQUEST)

    
    qs = Order.objects.filter(id=order.id)
    serializer = OrderSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
