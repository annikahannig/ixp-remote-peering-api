import urllib
from datetime import datetime

import requests

from django.core.cache import caches


class PeeringDBClient:
    """
    A client to the PeeringDB API.
    """

    def __init__(self, cache_ttl=864000, cache_size=8192):
        """Keep cache for 10d"""
        self._api_base = "https://peeringdb.com/api"
        self._session = requests.Session()
        self._cache = caches["default"]
        self._cache_ttl = cache_ttl
        self._api_calls = 0
        self._api_cache_misses = 0

    def _api_get_json(self, endpoint):
        """
        Call the PeeringDB API and return parsed data.

        Similar calls will be cached.  For caching, make sure to
        keep the order of arguments in the URL intact across
        all calls (foo=1&bar=2 != bar=2&foo=1).
        """

        self._api_calls += 1

        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        cached_response = self._cache.get(endpoint)
        if cached_response:
            return cached_response

        self._api_cache_misses += 1

        response = self._session.get(
            self._api_base + endpoint,
            headers={"Accept": "application/json"}
        ).json()

        self._cache.set(endpoint, response, self._cache_ttl)

        return response


    def org_by_id(self, org_id):
        org = self._api_get_json(
            "org?{}".format(urllib.urlencode({"id": org_id}))
        ).get("data", None)
        return org

    def net_by_asn(self, asn):
        net = self._api_get_json(
            "net?{}".format(urllib.urlencode({"asn": asn}))
        ).get("data", None)
        return net

    def name_by_asn(self, asn):
        net = self.net_by_asn(asn)
        if net:
            return net[0]["name"]
        else:
            return None

    def orgname_by_asn(self, asn):
        net = self.net_by_asn(asn)
        if not net:
            return None

        # Get Org info by org id:
        org = self.org_by_id(net[0]['org_id'])

        if not org:
            return None

        return org[0]['name']
