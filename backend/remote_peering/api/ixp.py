
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.core.exceptions import *
import numbers


class IxpViewSet(viewsets.ViewSet):
    def list(self, request):
        name = request.query_params.get('name')
        peering_id = request.query_params.get('peering_id')

        if name is not None and peering_id is not None:
            return response.Response({
                "status": 400,
                "message": "Please specify either a name or a peering db id"
            }, 400)

        if name is not None:
            entries = models.Ixp.objects.filter(name__icontains=name)
            entries = serializers.IxpSerializer(entries, many=True).data
        elif peering_id is not None:
            if isinstance(peering_id, numbers.Integral):
                entries = models.Ixp.objects.get(peeringdb_id=peering_id)
                entries = serializers.IxpSerializer(entries).data
            else:
                return response.Response({
                    "status": 400,
                    "message": "The PeeringDB id is an integer value"
                }, 400)
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
