

from rest_framework import routers, views, viewsets
from rest_framework.decorators import detail_route


from remote_peering.api import status


router = routers.DefaultRouter()
router.register('status', status.StatusViewSet, base_name='api-status')

