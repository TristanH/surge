from site.models import Keyword
from site.views.serializers import KeywordSerializer

# Sets define the view behavior [all models, for now just Keyword]             
class KeywordViewSet(viewsets.ModelViewSet):                                       
    queryset = Keyword.objects.all()                                               
    serializer_class = KeywordSerializer  
