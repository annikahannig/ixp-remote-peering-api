
from rest_framework import serializers

from remote_peering import models


class MemberAsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.As
        fields = ('id', 'number', 'created_at')
        depth = 1


class MemberSerializer(serializers.ModelSerializer):
    asn = MemberAsSerializer()

    class Meta:
        model = models.Member
        fields = ('id', 'name', 'asn')


class AsMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('id', 'name')


class AsSerializer(serializers.ModelSerializer):
    member = AsMemberSerializer(source='member_set', many=True)

    class Meta:
        model = models.As
        fields = ('id', 'number', 'created_at', 'member')
        depth = 1


class IxpSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = models.Ixp
        fields = ('id', 'name', 'members', 'locations', 'peeringdb_id')
        depth = 2


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'continent', 'country', 'city')


class IpSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    class Meta:
        model = models.Ip
        fields = ('id', 'address', 'version', 'longitude', 'latitude',
                  'member', 'locations', 'created_at')
        depth = 2


class IpMetricSerializer(serializers.ModelSerializer):
    ip = IpSerializer()

    class Meta:
        model = models.IpMetric
        fields = ('id', 'ip', 'median_rtt', 'created_at')
        depth = 2


class StatusSerializer(serializers.Serializer):
    last_run = serializers.DateTimeField()
