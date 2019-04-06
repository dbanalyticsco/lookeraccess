import requests
import logging
from utils import compose_url, filter_list

logging.basicConfig(level=logging.INFO)

class LookerConnection:

    def __init__(self, client_id, client_secret, url):

        if url[-1] == '/':
            self.url = url[:-1] + ':19999/api/3.0/'
        else:
            self.url = url + ':19999/api/3.0/'
        self.headers = self.connect(client_id, client_secret)

    def connect(self, client_id, client_secret):
        """Gets Access Token from Looker, setting token on LookerConnection"""

        login = requests.post(
            url=compose_url(self.url, 'login'),
            data={'client_id': client_id, 'client_secret': client_secret})
        logging.info("Connecting to Looker instance, url: {}".format(login.url))

        try:
            access_token = login.json()['access_token']
            headers = {'Authorization': 'token {}'.format(access_token)}
        except KeyError:
            logging.error('Incorrect Client Credentials')
            headers = None

        return headers
    
    def _get(self, endpoint, endpointid=None, subendpoint=None, subendpointid=None):
        
        r = requests.get(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers)

        if r.ok:
            return r.json()
        else:
            raise Exception('Get request unsuccessful, url: {}')

    def _delete(self, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.delete(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers)

        if r.ok:
            return r.json()
        else:
            raise Exception('Delete request unsuccessful, url: {}')

    def _patch(self, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.patch(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers,
            json=payload)

        if r.ok:
            return r.json()
        else:
            raise Exception('Patch request unsuccessful, url: {}')

    def _post(self, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.post(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers,
            json=payload)

        if r.ok:
            return r.json()
        else:
            raise Exception('Post request unsuccessful, url: {}')

    def get_model_sets(self):

        response = self._get('model_sets')
        keys = ['id','name','models']

        return filter_list(response, keys)

    def get_permission_sets(self):

        response = self._get('permission_sets')
        keys = ['id','name','permissions']

        return filter_list(response, keys)

    def get_roles(self):

        response = self._get('roles')
        keys = ['id','name','permission_set','model_set']

        filtered = filter_list(response, keys)

        for item in filtered:
            item['permission_set'] = { key: item['permission_set'][key] for key in ['id','name'] }
            item['model_set'] = { key: item['model_set'][key] for key in ['id','name'] }

        return filtered

    def get_role_users(self, role_id):

        response = self._get('roles', role_id, 'users')
        keys = ['id','email']

        return filter_list(response, keys)

    def get_role_groups(self, role_id):

        response = self._get('roles', role_id, 'groups')
        keys = ['id','name']

        return filter_list(response, keys)

    def get_groups(self):

        response = self._get('groups')
        keys = ['id','name']

        return filter_list(response, keys)

    def get_group_groups(self, group_id):

        response = self._get('groups', group_id, 'groups')
        keys = ['id','name']

        return filter_list(response, keys)

    def get_group_users(self, group_id):

        response = self._get('groups', group_id, 'users')
        keys = ['id','email']

        return filter_list(response, keys)

