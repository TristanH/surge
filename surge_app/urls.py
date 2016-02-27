from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

# REST API code
from site.models import Keyword
from rest_framework import routers, serializers, viewsets

# Serialization for [all models, for now just Keyword]
class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = ('string')

# ViewSets define the view behavior [all models, for now just Keyword]
class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'keywords', KeywordViewSet)

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', site.views.index, name='index'),
    url(r'^db', site.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
