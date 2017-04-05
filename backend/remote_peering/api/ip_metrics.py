
from rest_framework import viewsets, response

from remote_peering import models
from remote_peering.api import serializers





class IpMetricsViewSet(viewsets.ViewSet):
    def list(self, request):
        metrics = models.IpMetrics.objects.all()

        serializer = serializers.IpMetricSerializer(metrics, many=True)

        return response.Response({
            'metrics': serializer.data
        })

    def retrieve(self, request, pk=None):
        return response.Response({
            'pk': pk
        })
