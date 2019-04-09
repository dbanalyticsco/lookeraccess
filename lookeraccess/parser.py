import yaml
from datetime import datetime
import os
import json

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_looker_config(conn):

    config = {}

    print('Getting Permission Sets.')
    config['permission_sets'] = conn.get_permission_sets()
    print('Getting Model Sets.')
    config['model_sets'] = conn.get_model_sets()
    print('Getting Roles.')
    config['roles'] = enrich_roles(conn.get_roles(), conn)
    print('Getting Groups.')
    config['groups'] = enrich_groups(conn.get_groups(), conn)

    return config

def load_looker_config_from_logs():

    directory = max(os.listdir('./logs'))

    print('Loading Looker config from logs.')
    with open('logs/{}/config.json'.format(directory), 'r') as document:
        config = json.load(document)

    return config

def enrich_roles(roles, conn):

    print('Enriching Groups with Groups and Users.')
    for item in roles:
        print('    Enriching Role: {}'.format(item['name']))
        item['groups'] = conn.get_role_groups(item['id'])
        item['users'] = conn.get_role_users(item['id'])

    return roles

def enrich_groups(groups, conn):

    print('Enriching Roles with Groups and Users.')
    for item in groups:
        print('    Enriching Group: {}'.format(item['name']))
        item['groups'] = conn.get_group_groups(item['id'])
        item['users'] = conn.get_group_users(item['id'])

    return groups

def clean_looker_config(config):

    print('Starting cleaning of Looker configuration.')
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

        if group_groups == []:
            group.pop('groups')
        else: 
            group['groups'] = group_groups

        if group_users == []:
            group.pop('users')
        else:
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

        if role_groups == []:
            role.pop('groups')
        else: 
            role['groups'] = role_groups

        if role_users == []:
            role.pop('users')
        else:
            role['users'] = role_users

    print('Finished Cleaning of Looker configuration.')

    return config

def log_looker_config_file(conn, config, run_time, pull=False):

    if not os.path.exists('logs'):
        os.makedirs('logs')
    directory = 'logs/{}'.format(run_time.strftime("%Y%m%d-%H%M%S"))
    if not os.path.exists(directory):
        os.makedirs(directory)

    for key in config.keys():

        with open('{}/{}.yml'.format(directory,key),'w') as outfile:
            yaml.dump({key: config[key]}, outfile, default_flow_style=False, Dumper=Dumper)

    if pull:

        for key in config.keys():

            with open('{}.yml'.format(key),'w') as outfile:
                yaml.dump({key: config[key]}, outfile, default_flow_style=False, Dumper=Dumper)


def log_raw_looker_config_file(conn, config, run_time):
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    directory = 'logs/{}'.format(run_time.strftime("%Y%m%d-%H%M%S"))
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open('{}/config.json'.format(directory), 'w') as outfile:
        json.dump(config, outfile)








