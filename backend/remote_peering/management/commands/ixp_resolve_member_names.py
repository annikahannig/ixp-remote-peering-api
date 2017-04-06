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
            name = pdb.orgname_by_asn(member.asn.number)
            current = member.name
            if name == current:
                print("AS{} => {} still valid".format(
                    member.asn.number,
                    member.name))

            if name != current:
                member.name = name
                member.save()

                if current:
                    print("Changed name: {} for AS{}, was: {}".format(
                        name, member.asn.number, current))
                else:
                    print("Resolved name: {} for AS{}".format(
                        name, member.asn.number))


