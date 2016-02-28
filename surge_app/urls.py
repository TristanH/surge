from django.conf.urls import include, url

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

# REST API code
from main.views.views import *
from main.views.view_sets import *
from main.views.post_views import *
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# GET requests for REST
router.register(r'keywords_main', KeywordViewSetMain)
router.register(r'keywords_modifier', KeywordViewSetModifier)

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^bidding/?$', bidding, name='bidding'),
    url(r'^restaurant/(?P<restaurant_id>[0-9]+)/?$', restaurant_profile, name='restaurant_profile'),


    url(r'^login/?$', auth_views.login,
        {'template_name': 'login.html',},
        name='login'),
    url(r'^logout/', auth_views.logout),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Fancier requests for REST (this way is better)
    url(r'^new_order/(?P<pk>[0-9]+)$', new_order, name='new_order'),
    url(r'^get_orders/(?P<pk>[0-9]+)$', get_orders, name='get_orders'),
    url(r'^call_lyft/$', call_lyft, name='call_lyft'),
]
