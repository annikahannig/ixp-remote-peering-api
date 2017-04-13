
from rest_framework import viewsets, response

from remote_peering import models, utils, query
from remote_peering.api import serializers

from django.db.models import Q

import operator

from datetime import datetime


class IpMetricsViewSet(viewsets.ViewSet):
    """
    Retrieve and filter IP metrics.

    ### Date Querying
    * `?date=<date>` e.g. 2016-08-01T00:00:00Z or 2016-08-01
    * `?date__lt=<date>`
    * `?date__lte=<date>`
    * `?date__gt=<date>`
    * `?date__gte=<date>`

    ### Date range querying
    * `?date_start=<date>` Items with x > date)
    * `?date_end=<date>` Items with x <= date

    ### Query Parameters
    * `?ip=<ip address>`
    * `?ips=<ip address>[,<ip address>...]`
    * `?asn=<as number>`
    * `?asns=<as_number>[,<as number>...]`
    * `?median_rtt__<lt|lte|gt|gte>=<float>`

    ### Pagination
    * `?limit=<number>`
    * `?start=<number>`
    """

    def list(self, request):

        # Query Schema
        filters = query.filters_from_query_params(request.query_params, {
            'date': ('created_at', datetime, 'lt', 'lte', 'gt', 'gte'),
            'date_start': ('created_at', range, datetime, 'gt' ),
            'date_end': ('created_at', range, datetime, 'lte' ),

            'ip': ('ip__address', str, 'contains'),
            'ips': ('ip__address', [str], ),

            'asn': ('ip__member__asn__number', int, ),
            'asns': ('ip__member__asn__number', [int], ),

            'median_rtt': ('median_rtt', float, 'lt', 'lte', 'gt', 'gte')
        })

        # Limiting
        start = int(request.query_params.get('start', 0))
        limit = request.query_params.get('limit', None)
        end = int(limit) + start if limit else None

        # Done. Combine all query parameters
        if filters:
            entries = models.IpMetric.objects.filter(filters)[start:end]
        else:
            entries = models.IpMetric.objects.all()[start:end]

        entries = serializers.IpMetricSerializer(entries, many=True).data

        return response.Response({
            "status": 200,
            "start": start,
            "limit": int(limit) if limit else 0,
            "count": len(entries),
            "data": entries
        })
