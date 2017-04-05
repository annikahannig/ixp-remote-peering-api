
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers


class IpMetricsViewSet(viewsets.ViewSet):
    def list(self, request):
        entries = models.IpMetric.objects.all()
        entries = serializers.IpMetricSerializer(entries, many=True)

        return response.Response({
            "status": 200,
            "data": entries.data
        })
