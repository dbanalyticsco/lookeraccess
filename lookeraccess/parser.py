import yaml
from datetime import datetime
import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_looker_config(conn):

    config = {}

    config['permission_sets'] = conn.get_permission_sets()
    config['model_sets'] = conn.get_model_sets()
    config['roles'] = enrich_roles(conn.get_roles(), conn)
    config['groups'] = enrich_groups(conn.get_groups(), conn)

    return config

def enrich_roles(roles, conn):

    for item in roles:
        item['groups'] = conn.get_role_groups(item['id'])
        item['users'] = conn.get_role_users(item['id'])

    return roles

def enrich_groups(groups, conn):

    for item in groups:
        item['groups'] = conn.get_group_groups(item['id'])
        item['users'] = conn.get_group_users(item['id'])

    return groups

def prep_looker_config_for_log(config):

    config['permission_sets'] = [item for item in config['permission_sets'] if item['name'] != 'Admin']
    config['model_sets'] = [item for item in config['model_sets'] if item['name'] != 'All']
    config['groups'] = [item for item in config['groups'] if item['name'] != 'All Users']

    for key in ['permission_sets','model_sets']:
        for item in config[key]:
            item.pop('id')

    for group in config['groups']:
        group.pop('id')
        group_users = []
        group_groups = []
        for item in group['groups']:
            group_groups.append(item['name'])
        for item in group['users']:
            group_users.append(item['email'])
        group_groups.sort()
        group_users.sort()
        group['groups'] = group_groups
        group['users'] = group_users

    for role in config['roles']:
        role.pop('id')
        role['permission_set'] = role['permission_set']['name']
        role['model_set'] = role['model_set']['name']
        
        role_users = []
        role_groups = []
        for item in role['groups']:
            role_groups.append(item['name'])
        for item in role['users']:
            if item['email']:
                role_users.append(item['email'])
        role_groups.sort()
        role_users.sort()
        role['groups'] = role_groups
        role['users'] = role_users

    return config

def log_looker_config_file(conn, pull=False):

    config = get_looker_config(conn)
    prepped = prep_looker_config_for_log(config)

    if not pull:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        directory = 'logs/{}/'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        os.makedirs(directory)
    else:
        directory = ''

    for key in prepped.keys():

        with open('{}{}.yml'.format(directory,key),'w') as yaml_file:
            yaml.dump({key: prepped[key]}, yaml_file, default_flow_style=False, Dumper=Dumper)





