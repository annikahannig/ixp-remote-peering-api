
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.core.exceptions import *


class AsnViewSet(viewsets.ViewSet):
    def list(self, request):
        entries = models.As.objects.all()
        entries = serializers.AsSerializer(entries, many=True)

        return response.Response({
            "status": 200,
            "data": entries.data
        })

    def retrieve(self, request, pk=None):
        try:
            asn = models.As.objects.get(pk=pk)
            asn = serializers.AsSerializer(asn).data
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
