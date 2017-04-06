from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from remote_peering import models
from remote_peering.services import peeringdb

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Resolve all member names"""
        pdb = peeringdb.PeeringDBClient()

        members = models.Member.objects.all().prefetch_related('asn')
        for member in members:
            if member.name:
                continue
            name = pdb.orgname_by_asn(member.asn.number)
            if name:
                member.name = name
                member.save()

                print("Resolved {} for AS{}".format(name, member.asn.number))

