
from rest_framework import serializers

from remote_peering import models


class AsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.As
        fields = ('number', 'created_at')


