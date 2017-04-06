
from rest_framework import viewsets, response
from remote_peering import models
from remote_peering.api import serializers
from django.core.exceptions import *


class AsnViewSet(viewsets.ViewSet):
    def list(self, request):
        number = request.query_params.get('number')

        start = request.query_params.get('start')
        start = int(start) if start else 0

        limit = request.query_params.get('limit')
        end = int(limit) + start if limit else None

        if number is not None:
            entries = models.As.objects.get(number=number)[start:end]
            entries = serializers.AsSerializer(entries).data
        else:
            entries = models.As.objects.all()[start:end]
            entries = serializers.AsSerializer(entries, many=True).data

        return response.Response({
            "status": 200,
            "start": int(start),
            "limit": int(limit) if limit else 0,
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
