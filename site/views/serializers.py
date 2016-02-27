from site.models import Keyword

# Serialization for [all models, for now just Keyword]                             
class KeywordSerializer(serializers.HyperlinkedModelSerializer):                   
    class Meta:                                                                    
        model = Keyword                                                            
        fields = ('string') 
