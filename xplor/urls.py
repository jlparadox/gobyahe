from django.conf.urls import *
from xplor import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^itinerary/add/$', views.itinerary_add, name='home_itinerary_add'),
    url(r'^search/', include('haystack.urls')),
]