from main.models import Keyword, Order
from rest_framework import serializers

# Serialization for [all models, for now just Keyword]                             
class KeywordSerializer(serializers.HyperlinkedModelSerializer):                   
    class Meta:                                                                    
        model = Keyword                                                            
        fields = ('string', 'is_main',)

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('hungry_user')
