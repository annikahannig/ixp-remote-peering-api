
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
    * `?date=<date>` e.g. 2016-08-01T00:00:00Z
    * `?day=<1-31>`
    * `?month=<1-12>`
    * `?year=<yyyy>`

    ### Query Parameters
    * `?ip=<ip address>[,<ip address>...]`
    * `?asn=<as number>[,<as number>...]`
    * `?median_rtt_<lte|gte>=<float>`

    ### Pagination
    * `?limit=<number>`
    * `?start=<number>`
    """

    def list(self, request):

        # Date filtering
        created_at = request.query_params.get('date')
        date_day = request.query_params.get('day')
        date_month = request.query_params.get('month')
        date_year = request.query_params.get('year')


        ip_address = query.params_list(request, 'ip')
        asn = utils.params_list(request,'asn')
        median_rtt_lte = request.query_params.get('median_rtt_lte')
        median_rtt_gte = request.query_params.get('median_rtt_gte')

        filters = utils.filters_from_query_params(request.query_params, {
            'date': (datetime,),
            'date_start': (datetime, 'lt','lte', 'gt', 'gte'),
            'date_end': (datetime, 'lt', 'lte', 'gt', 'gte'),

            'ips': ([str], ),
            'ip':, (str, 'contains'),

            'asns': ([int], ),
            'asn': (int, ),


            'median_rtt', (float, 'lt', 'lte', 'gt', 'gte')
        })

        # Limiting
        start = int(request.query_params.get('start', 0))
        limit = request.query_params.get('limit', None)
        end = int(limit) + start if limit else None

        query_list = []

        if created_at:
            query_list.append(Q(created_at=created_at))

        if date_day:
            query_list.append(Q(created_at__day=date_day))

        if date_month:
            query_list.append(Q(created_at__month=date_month))

        if date_year:
            query_list.append(Q(created_at__year=date_year))

        if ip_address:
            query_list.append(Q(ip__address__in=ip_address))

        if asn:
            query_list.append(Q(ip__member__asn__number__in=asn))

        if median_rtt_gte:
            query_list.append(Q(median_rtt__gte=median_rtt_gte))

        if median_rtt_lte:
            query_list.append(Q(median_rtt__lte=median_rtt_lte))

        # Done. Combine all query parameters
        if query_list:
            entries = models.IpMetric.objects\
                .filter(reduce(operator.and_, query_list))[start:end]
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
