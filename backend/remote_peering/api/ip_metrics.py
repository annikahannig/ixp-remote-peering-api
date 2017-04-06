
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.db.models import Q
import operator


class IpMetricsViewSet(viewsets.ViewSet):
    def list(self, request):
        created_at = request.query_params.get('date')
        ip_v4 = request.query_params.get('ip_v4')
        asn = request.query_params.get('asn')
        median_rtt_lt = request.query_params.get('median_rtt_lt')
        median_rtt_gt = request.query_params.get('median_rtt_gt')

        query_list = []

        if created_at is not None:
            query_list.append(Q(created_at=created_at))

        if ip_v4 is not None:
            query_list.append(Q(ip__address=ip_v4))
            query_list.append(Q(ip__version=4))

        if asn is not None:
            query_list.append(Q(ip__member__asn__number=asn))

        if created_at is not None or ip_v4 is not None or asn is not None:
            entries = models.IpMetric.objects\
                .filter(reduce(operator.and_, query_list))
        else:
            entries = models.IpMetric.objects.all()

        entries = serializers.IpMetricSerializer(entries, many=True)

        return response.Response({
            "status": 200,
            "data": entries.data
        })
