
from rest_framework import serializers

from remote_peering import models


class AsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.As
        fields = ('number', 'created_at', 'member_set')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('asn', 'name')
        depth = 2


class IxpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ixp
        fields = ('name', 'members', 'locations', 'peeringdb_id')
        depth = 2


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('continent', 'country', 'city')


