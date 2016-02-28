from main.models import Keyword, Order, Item, Bid
from rest_framework import serializers

# Serialization for [all models, for now just Keyword]                             
class KeywordSerializer(serializers.HyperlinkedModelSerializer):                   
    class Meta:                                                                    
        model = Keyword                                                            
        fields = ('string', 'is_main',)

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('description', 'latitude', 'longitude',)

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description')

class BidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ('won')
