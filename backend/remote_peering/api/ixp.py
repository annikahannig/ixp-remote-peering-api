
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.core.exceptions import *


class IxpViewSet(viewsets.ViewSet):
    def list(self, request):
        name = request.query_params.get('name')
        peering_id = request.query_params.get('peering_id')

        if name is not None and peering_id is not None:
            return response.Response({
                "status": 400,
                "message": "Please specify either a name or a peering db id"
            })

        if name is not None:
            entries = []
        elif peering_id is not None:
            entries = []
        else:
            entries = models.Ixp.objects.all()
            entries = serializers.IxpSerializer(entries, many=True).data

        return response.Response({
            "status": 200,
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
