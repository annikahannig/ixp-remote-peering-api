
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


class AsIxpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ixp
        fields = ('id', 'name')


class AsMemberSerializer(serializers.ModelSerializer):
    ixps = AsIxpSerializer(source='ixp_set', many=True)

    class Meta:
        model = models.Member
        fields = ('id', 'name', 'ixps')
        depth = 2


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
                  'member', 'locations', 'num_paths', 'num_peerings',
                  'created_at')
        depth = 2

class IpMetricIxpSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ixp
        fields = ('id', 'name', 'peeringdb_id')


class IpMetricSerializer(serializers.ModelSerializer):
    ip = IpSerializer()
    ixp = IpMetricIxpSerializer()

    class Meta:
        model = models.IpMetric
        fields = ('id', 'ip', 'median_rtt', 'created_at', 'ixp')
        depth = 2


class StatusSerializer(serializers.Serializer):
    last_run = serializers.DateTimeField()
