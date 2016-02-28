from main.models import Keyword
from rest_framework import viewsets
from main.views.serializers import KeywordSerializer

# Sets define the view behavior [all models, for now just Keyword]             
class KeywordViewSetMain(viewsets.ModelViewSet):                                       
    queryset = Keyword.objects.filter(is_main=True)
    serializer_class = KeywordSerializer  

class KeywordViewSetModifier(viewsets.ModelViewSet):
    queryset = Keyword.objects.filter(is_main=False)
    serializer_class = KeywordSerializer
    