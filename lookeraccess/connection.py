import requests
import logging
from lookeraccess.utils import compose_url, filter_list

logging.basicConfig(level=logging.INFO)

class LookerConnection:

    def __init__(self, client_id, client_secret, url, port=19999):

        if url[-1] == '/':
            self.url = '{}:{}/api/3.0/'.format(url[:-1], port)
        else:
            self.url = '{}:{}/api/3.0/'.format(url, port)
        self.headers = self.connect(client_id, client_secret)

    def connect(self, client_id, client_secret):
        """Gets Access Token from Looker, setting token on LookerConnection"""

        login = requests.post(
            url=compose_url(self.url, 'login'),
            data={'client_id': client_id, 'client_secret': client_secret})

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
            raise Exception('Get request unsuccessful, url: {}'.format(r.url))

    def _delete(self, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.delete(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers)

    def _patch(self, payload, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.patch(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers,
            json=payload)

        if r.ok:
            return r.json()
        else:
            raise Exception('Patch request unsuccessful, url: {}'.format(r.url))

    def _post(self, payload, endpoint, endpointid=None, subendpoint=None, subendpointid=None):

        r = requests.post(
            url=compose_url(self.url, endpoint, endpointid=endpointid, subendpoint=subendpoint, subendpointid=None),
            headers=self.headers,
            json=payload)

        if r.ok:
            return r.json()
        else:
            raise Exception('Post request unsuccessful, url: {}'.format(r.url))

    def get_model_sets(self):

        response = self._get('model_sets')
        keys = ['id','name','models']

        return filter_list(response, keys)

    def get_permission_sets(self):

        response = self._get('permission_sets')
        keys = ['id','name','permissions']

        return filter_list(response, keys)

    def get_all_permissions(self):

        response = self._get('permissions')
        keys = ['permission']

        return filter_list(response, keys)

    def get_all_models(self):

        response = self._get('lookml_models')
        keys = ['name']

        return filter_list(response, keys)

    def get_all_users(self):

        response = self._get('users')
        keys = ['email']

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

    def create_permission_set(self, name, permissions):

        self._post(
                payload={'name': name, 'permissions': permissions},
                endpoint='permission_sets'
            )

    def update_permission_set(self, object_id, name, permissions):

        self._patch(
                payload={'name': name, 'permissions': permissions},
                endpoint='permission_sets',
                endpointid=object_id
            )

    def delete_permission_set(self, object_id):

        self._delete(endpoint='permission_sets',endpointid=object_id)

    def create_model_set(self, name, models):

        self._post(
                payload={'name': name, 'models': models},
                endpoint='model_sets'
            )

    def update_model_set(self, object_id, name, models):

        self._patch(
                payload={'name': name, 'models': models},
                endpoint='model_sets',
                endpointid=object_id
            )

    def delete_model_set(self, object_id):

        self._delete(endpoint='model_sets',endpointid=object_id)

    def create_group(self, name):

        self._post(
                payload={'name': name},
                endpoint='groups'
            )

    def add_group_to_group(self, group_id, sub_group_id):

        self._post(
                payload={'group_id': sub_group_id},
                endpoint='groups',
                endpointid=group_id,
                subendpoint='groups'
            )

    def delete_group(self, object_id):

        self._delete(endpoint='groups',endpointid=object_id)



