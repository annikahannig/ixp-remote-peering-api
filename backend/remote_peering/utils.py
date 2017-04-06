

def params_list(request, param):
    """Returns a list of csv params"""
    params = [p.strip() for p
              in request.query_params.get(param, '').split(',')
              if p]
    return params



