

"""
Remote Peering API
"""
from django.conf import settings
from django.conf.urls import url, include

from remote_peering import views

urlpatterns = [
    url(r'^$', views.welcome),
    url(r'^api/', views.api_stub),
]

