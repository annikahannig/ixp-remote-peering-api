

"""
Test filter generation
"""

from __future__ import unicode_literals

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
        'foo': (float, ),
        'foos': ([int], ),
        'bar': (str, 'icontains'),
        'baz': (int, 'lt'),
    }

    whitelist_params = filters.whitelist_params(params, schema)

    assert 'bar__baz' not in whitelist_params.keys()
    assert 'bar__icontains' in whitelist_params.keys()
    assert 'foos__in' in whitelist_params.keys()

    assert whitelist_params['foo'] == 42
    assert whitelist_params['foos__in'] == [23, 42]
    assert whitelist_params['bar__icontains'] == 'test'

    assert whitelist_params['baz'] == 42
    assert whitelist_params['baz__lt'] == 42

