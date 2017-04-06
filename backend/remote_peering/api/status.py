
from rest_framework import viewsets, response

from remote_peering.services import ip_metrics
from remote_peering.api import serializers

class StatusViewSet(viewsets.ViewSet):
    """Just some base view"""
    def list(self, request):
        # Get information about last imported data
        last_run_date = ip_metrics.last_import_date()
        result = serializers.StatusSerializer({
            "last_run": last_run_date,
        })

        return response.Response({
            'status': 200,
            'data': result.data,
        })
