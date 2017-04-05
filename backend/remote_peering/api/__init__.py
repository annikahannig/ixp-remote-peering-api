

from rest_framework import routers, views, viewsets
from rest_framework.decorators import detail_route


from remote_peering.api import status
from remote_peering.api import ixp
from remote_peering.api import asn
from remote_peering.api import ip_metrics


router = routers.DefaultRouter()
# API status
router.register('status', status.StatusViewSet, base_name='api-status')

# IXP related resources
router.register('ixp', ixp.IxpViewSet, base_name='api-ixp')

# ASN related resources
router.register('asn', asn.AsnViewSet, base_name='api-asn')

# IP Metrics related resources
router.register('metrics/ip', ip_metrics.IpMetricsViewSet, base_name='api-ip-metrics')

