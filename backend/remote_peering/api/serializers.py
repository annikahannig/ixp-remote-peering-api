
from rest_framework import serializers

from remote_peering import models

class IpMetricSerializer(serializers.ModelSerializer):


    class Meta:
            model = models.IpMetric
            fields = ('id', 'median_rtt', 'ip', 'created_at')


