# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models



class As(models.Model):
    number = models.IntegerField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    continent = models.CharField(max_length=80)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)

    class Meta:
        unique_together = ('continent', 'country', 'city',)


class Member(models.Model):

    asn = models.ForeignKey(As, null=False, blank=False)
    name = models.CharField(max_length=80, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Ixp(models.Model):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(Member)
    locations = models.ManyToManyField(Location)

    peeringdb_id = models.IntegerField(unique=True)




class Ip(models.Model):
    address = models.CharField(max_length=100)
    version = models.IntegerField(default=6)

    longitude = models.FloatField()
    latitude = models.FloatField()

    member = models.ForeignKey(Member)

    created_at = models.DateTimeField(auto_now_add=True)


class IpMetric(models.Model):
    ip = models.ForeignKey(Ip)
    median_rtt = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)




