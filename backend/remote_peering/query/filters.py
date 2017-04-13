
from __future__ import unicode_literals

from django.db.models import Q
from django.utils import dateparse, timezone

from datetime import datetime, time

import operator
import functools

def _params_list(t, param):
    """Returns a list of csv params cast to type t"""
    params = [t(p.strip()) for p
              in param.split(',')
              if p]
    return params


def _parse_date(string):
    """Return timezone aware datetime from input"""
    if " " in string:
        result = dateparse.parse_datetime(string)
    else:
        result = datetime.combine(
            dateparse.parse_date(string),
            time())

    # Make tz aware
    return timezone.utc.localize(result)


def _query_type(param_schema):
    """Get type from param schema"""
    p_type = param_schema[0]
    if p_type == datetime:
        p_type = _parse_date
    elif type(p_type) == list:
        p_type = functools.partial(_params_list, p_type[0])
    elif p_type == range:
        p_type = _query_type(param_schema[1:])
    return p_type


def _query_modifiers(param_schema):
    """Get whitelisted modifiers"""
    if param_schema[0] == range:
        return param_schema[2:]
    return param_schema[1:]


def whitelist_params(params, schema):
    """
    Make a filtered whitelisted list of params
    """
    filtered = {}
    for param, value in params.iteritems():
        tokens = param.split('__', 2)
        param = tokens[0]

        modifier = tokens[1] if len(tokens) == 2 else None

        # Check param whitelist
        if schema.get(param) == None:
            continue # Param not whitelisted

        # Check modifier whitelist
        modifier_whitelist = _query_modifiers(schema[param])
        if modifier and not modifier in modifier_whitelist:
            continue # modifier not whitelisted

        # Automodifier
        s_type = schema[param][0] # Schema type
        q_type = _query_type(schema[param])
        if type(s_type) == list:
            modifier = 'in'
        elif s_type == range:
            modifier = schema[param][2]

        q_value = q_type(value)

        # Make query filter with param name and
        # whitelisted modifier:
        if modifier:
            q_param = "{}__{}".format(param, modifier)
        else:
            q_param = param

        filtered[q_param] = q_value

    return filtered


def filters_from_query_params(params, schema):
    """
    Converts query params to filters using a schema.
    The schema consists of a the name of the
    whitelisted queryparam, the type and and a list
    of allowed modifiers (like __lt, __in, __icontains, ...).

    If the type is wrapped in an array an implicit __in is
    applied.


    Example:

        'names': ([str], ),
        'name': (str, 'icontains', 'contains'),

    If the type starts with range, the parameter subsequent
    to the desired type will be used as modifier:

    Example:

        'date_start': (range, datetime, 'gte')

    will result in a timezone aware datetime query:
        'date_start__gte': datetime(...)

    """
    filtered_params = whitelist_params(params, schema)
    filters = reduce(operator.and_, [Q(**{param: value})
                                     for param, value
                                     in filtered_params.iteritems()])
    return filters
