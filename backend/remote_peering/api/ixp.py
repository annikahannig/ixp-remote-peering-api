
from rest_framework import viewsets, response


class IxpViewSet(viewsets.ViewSet):
    """Just some base view"""
    def list(self, request):
        return response.Response({
            'status': 'OK'
        })

    def retrieve(self, request, pk=None):
        return response.Response({
            'pk': pk
        })
