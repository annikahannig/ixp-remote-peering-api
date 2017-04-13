

"""
Test filter generation
"""

from __future__ import unicode_literals

from django.db.models import Q
from django.utils import timezone

from datetime import datetime
from remote_peering.query import filters


def test_filters_whitelist():
    """Test query params"""

    params = {
        'foo': '42',
        'foos': '23,42',
        'bar__icontains': 'test',
        'bar__baz': 'foo',
        'baz': '42',
        'baz__lt': '42',
    }

    schema = {
        'foo': ('foo', float, ),
        'foos': ('foo', [int], ),
        'bar': ('bar', str, 'icontains'),
        'baz': ('baz', int, 'lt'),
    }

    whitelist_params = filters.whitelist_params(params, schema)

    assert 'bar__baz' not in whitelist_params.keys()
    assert 'bar__icontains' in whitelist_params.keys()
    assert 'foo__in' in whitelist_params.keys()

    assert whitelist_params['foo'] == 42
    assert whitelist_params['foo__in'] == [23, 42]
    assert whitelist_params['bar__icontains'] == 'test'

    assert whitelist_params['baz'] == 42
    assert whitelist_params['baz__lt'] == 42


def test_date_parsing():
    """Test date handling in queryparams"""
    params = {
        'foo': '2016-2-15',
        'bar_start': '2016-10-15 23:15:10',
        'bar_end': '2016-11-15 23:15:10',
    }

    schema = {
        'foo': ('foo', datetime, 'lt', 'lte'),
        'bar_start': ('bar', range, datetime, 'gt'),
        'bar_end': ('bar', range, datetime, 'lte'),
    }

    whitelist_params = filters.whitelist_params(params, schema)

    assert whitelist_params['foo'] == timezone.utc.localize(
        datetime(2016, 2, 15))
    assert whitelist_params['bar__gt'] == timezone.utc.localize(
        datetime(2016, 10, 15, 23, 15, 10))
    assert whitelist_params['bar__lte'] == timezone.utc.localize(
        datetime(2016, 11, 15, 23, 15, 10))



def test_from_query_params():

    params = {
        'foo': '42',
        'foos': '23,42',
    }

    schema = {
        'foo': ('foo', float, ),
        'foos': ('foo', [int], ),
    }

    f = filters.filters_from_query_params(params, schema)
    assert str(f) == str(Q(**{'foo': 42.0}) & Q(**{'foo__in': [23, 42]}))


def test_empty_params():
    params = {}
    schema = { 'foo': ('foo', int, ) }

    f = filters.filters_from_query_params(params, schema)

