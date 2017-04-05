
from rest_framework import viewsets, response
from remote_peering import models
from django.core.exceptions import *


class AsnViewSet(viewsets.ViewSet):
    def list(self, request):
        return response.Response(models.As.objects.all())

    def retrieve(self, request, pk=None):
        try:
            asn = models.As.objects.get(pk=pk)
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

        return response.Response({"status": 200, "data": asn})
