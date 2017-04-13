
from __future__ import unicode_literals

def _params_list(param, t):
    """Returns a list of csv params cast to type t"""
    params = [t(p.strip()) for p
              in param.split(',')
              if p]
    return params


def _query_type(param_schema):
    """Get type from param schema"""
    return param_schema[0]


def _query_modifiers(param_schema):
    """Get whitelisted modifiers"""
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
        q_type = _query_type(schema[param])
        if type(q_type) == list:
            modifier = 'in'
            p_type = q_type[0]
            q_value = _params_list(value, p_type)
        else:
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

    """

    return []
