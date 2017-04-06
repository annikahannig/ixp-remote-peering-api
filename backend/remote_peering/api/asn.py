
from django.core.exceptions import *
from rest_framework import viewsets, response

from remote_peering import models
from remote_peering.api import serializers

from remote_peering import utils

class AsnViewSet(viewsets.ViewSet):
    """
    Retrieve and filter a list of ASNs.

    ### Supported QueryParameters:

    * `?number=<asn>[,<asn>...]`
    """

    def list(self, request):
        asns = utils.params_list(request, 'number')
        if asns:
            results = models.As.objects.filter(number__in=asns)
        else:
            results = models.As.objects.all()


        entries = serializers.AsSerializer(results, many=True).data
        return response.Response({
            "status": 200,
            "count": len(entries),
            "data": entries
        })

    def retrieve(self, request, pk=None):
        try:
            asn = models.As.objects.get(pk=pk)
            asn = [serializers.AsSerializer(asn).data]
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
            "data": asn
        })
