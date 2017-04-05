

"""
Remote Peering API
"""
from django.conf import settings
from django.conf.urls import url, include

from remote_peering import views
from remote_peering import api

urlpatterns = [
    url(r'^$', views.welcome),
    url(r'^api/', include(api.router.urls)),
]

