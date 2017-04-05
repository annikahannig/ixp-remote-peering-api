
from rest_framework import viewsets, response


class StatusViewSet(viewsets.ViewSet):
    """Just some base view"""
    def list(self, request):
        return response.Response({
            'status': 'OK',
            'last_run': '2017-04-05'
        })
