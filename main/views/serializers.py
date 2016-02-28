from main.models import Keyword, Order, Item, KeywordGroup
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
    # description = serializers.CharField(max_length=511)

    class Meta:
        model = Order
        fields=('bidding_end_time', 'keywords', 'latitude', 'longitude', 'description')
        depth = 1
        # fields = ('description', 'bidding_end_time', 'keywords')

class ItemSerializer(serializers.ModelSerializer):
    keywords=KeywordGroupSerializer()

    class Meta:
        model = Item
        fields=('name', 'restaurant', 'keywords', 'description')
        depth = 1
