from django.utils import timezone

from main.models import Keyword, Order, Item, KeywordGroup, Bid

from rest_framework import serializers

# Serialization for [all models, for now just Keyword]                             
class KeywordSerializer(serializers.ModelSerializer):                   
    class Meta:                                                                    
        model = Keyword                                                            
        fields = ('string', 'is_main',)

class KeywordGroupSerializer(serializers.HyperlinkedModelSerializer):                   
    tags = KeywordSerializer

    class Meta:                                                                    
        model = KeywordGroup
        depth=1
        fields=('tags',)        


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=('id', 'bidding_end_time', 'keywords', 'latitude', 'longitude', 'description')
        depth = 2
        # fields = ('description', 'bidding_end_time', 'keywords')


class ItemSerializer(serializers.ModelSerializer):
    keywords=KeywordGroupSerializer()

    class Meta:
        model = Item
        fields=('id', 'name', 'restaurant', 'keywords', 'description')
        depth = 1


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        depth=1
