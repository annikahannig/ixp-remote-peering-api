
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.core.exceptions import *


class IxpViewSet(viewsets.ViewSet):
    def list(self, request):
        entries = models.Ixp.objects.all()
        entries = serializers.AsSerializer(entries, many=True)

        return response.Response({
            "status": 200,
            "data": entries.data
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
