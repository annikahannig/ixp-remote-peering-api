
from rest_framework import serializers

from remote_peering import models


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('name')


class AsSerializer(serializers.ModelSerializer):
    member_set = MemberSerializer()

    class Meta:
        model = models.As
        fields = ('number', 'created_at', 'member_set')
        depth = 1


class IxpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ixp
        fields = ('name', 'members', 'locations', 'peeringdb_id')
        depth = 2


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('continent', 'country', 'city')


