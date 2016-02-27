from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import main.views
# REST API code
from main.models import Keyword
from main.views.viewsets import *
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'keywords', viewsets.KeywordViewSet)

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', main.views.index, name='index'),
    url(r'^db', main.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
