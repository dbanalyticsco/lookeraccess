import yaml

def compose_url(urlbase, endpoint, endpointid=None, subendpoint=None, subendpointid=None):
    """
    Composes a URL from a base, endpoint and possible an endpoint ID and a sub-endpoint.
    Requires at least URL base and endpoint
    """

    if not urlbase or not endpoint:
        raise Exception('compose_url requires urlbase and endpoint.')

    url = "{}{}".format(urlbase,endpoint)

    if endpointid:
        url += '/' + str(endpointid)

        if subendpoint:
            url += '/' + subendpoint

            if subendpointid:
                url += '/' + subendpointid

    return url

def filter_list(items, keys):

    output = []

    for item in items:
        new_item = {key: item[key] for key in keys}
        output.append(new_item)

    return output

def read_yaml_file_from_path(self, path):
    with open(path, 'r') as stream:
        try:
            config = yaml.load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
