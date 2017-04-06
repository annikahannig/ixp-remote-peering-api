
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
        median_rtt_lte = request.query_params.get('median_rtt_lte')
        median_rtt_gte = request.query_params.get('median_rtt_gte')

        query_list = []

        if created_at is not None:
            query_list.append(Q(created_at=created_at))

        if ip_v4 is not None:
            query_list.append(Q(ip__address=ip_v4))
            query_list.append(Q(ip__version=4))

        if asn is not None:
            query_list.append(Q(ip__member__asn__number=asn))

        if median_rtt_gte is not None:
            query_list.append(Q(median_rtt__gte=median_rtt_gte))

        if median_rtt_lte is not None:
            query_list.append(Q(median_rtt__lte=median_rtt_lte))

        if query_list:
            entries = models.IpMetric.objects\
                .filter(reduce(operator.and_, query_list))
        else:
            entries = models.IpMetric.objects.all()

        entries = serializers.IpMetricSerializer(entries, many=True)

        return response.Response({
            "status": 200,
            "data": entries.data
        })
