


"""
Ip Metrics Access
"""

from remote_peering import models

def last_import_date():
    """Returns the last run date"""
    latest = models.IpMetric.objects.order_by('-created_at').first()
    if not latest:
        return None
    return latest.created_at


