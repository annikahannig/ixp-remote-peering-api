

from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers

from django.db.models import Q
from django.core.exceptions import *

import operator

class IxpViewSet(viewsets.ViewSet):
    """
    Retrieve and filter a list of IXPs and their members.

    ### Query Parameters:
    * `?name=<string>` Filter by IXP name
    * `?peeringdb_id=<int>` Filter by PeeringDB Id of IXP
    * `?member=<string>` Filter by name of member (contains, case insensitive)

    ###
    * `?start=<int>`
    * `?limit=<int>`
    """

    def list(self, request):
        ixp_name = request.query_params.get('name')
        peeringdb_id = request.query_params.get('peeringdb_id')

        start = int(request.query_params.get('start', 0))
        limit = request.query_params.get('limit', None)

        end = int(limit) + start if limit else None

        member_name = request.query_params.get('member')

        filters = []
        if ixp_name:
            filters.append(Q(name__icontains=ixp_name))

        if peeringdb_id:
            filters.append(Q(peeringdb_id=peeringdb_id))

        if member_name:
            filters.append(Q(members__name__icontains=member_name))


        if filters:
            ixp_filter = reduce(operator.and_, filters)
            ixps = models.Ixp.objects.filter(ixp_filter)
        else:
            ixps = models.Ixp.objects.all()

        entries = serializers.IxpSerializer(ixps[start:end], many=True).data
        return response.Response({
            "status": 200,
            "start": start,
            "limit": int(limit) if limit else 0,
            "count": len(entries),
            "data": entries
        })


    def retrieve(self, request, pk=None):
        try:
            ixp = models.Ixp.objects.get(pk=pk)
            ixp = serializers.IxpSerializer(ixp).data
        except MultipleObjectsReturned:
            return response.Response({
                "status": 400,
                "message": "Multiple records identified"
            }, 400)
        except ObjectDoesNotExist:
            return response.Response({
                "status": 404,
                "message": "Object does not exist"
            }, 404)

        return response.Response({
            "status": 200,
            "data": ixp
        })
