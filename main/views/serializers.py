from main.models import Keyword
from rest_framework import serializers

# Serialization for [all models, for now just Keyword]                             
class KeywordSerializer(serializers.HyperlinkedModelSerializer):                   
    class Meta:                                                                    
        model = Keyword                                                            
        fields = ('string') 
