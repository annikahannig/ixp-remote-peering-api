
from rest_framework import viewsets, response

from remote_peering import models

class AsnViewSet(viewsets.ViewSet):
    def list(self, request):
        asns = models.As.objects.all()
        result = [asn.number for asn in asns]

        return response.Response({
            "asns": result,
        })

    def retrieve(self, request, pk=None):
        return response.Response({
            'pk': pk
        })

