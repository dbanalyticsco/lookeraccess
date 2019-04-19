import yaml
import networkx as nx

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
                url += '/' + str(subendpointid)

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

def generate_groups_dag(config):

    G = nx.DiGraph()
    for group in config:
        
        if group['name'] not in G:
            G.add_node(group['name'])

        if 'groups' in group:
            for subgroup in group['groups']:
                if subgroup not in G:  
                    G.add_node(subgroup)
                G.add_edge(subgroup, group['name'])

    try:
        for node in nx.topological_sort(G):
            pass
    except nx.exception.NetworkXUnfeasible:
        print("Your groups can't be members of each other.")
        raise Exception("Two groups can't be members of each other.")
        
    return G
