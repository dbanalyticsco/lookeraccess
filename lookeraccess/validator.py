from schema import Schema, And, Use, Optional
from utils import generate_groups_dag


def check_keys(config):

	config_keys = config.keys()
	required_keys = ['model_sets','permission_sets','roles','groups']

	for key in config_keys:
		if key not in required_keys:
			raise Exception("'{}' cannot be accepted as a key in your configuration files.".format(key))

	for key in required_keys:
		if key not in config_keys:
			raise Exception("'{}' is missing from your configuration files.".format(key))


def check_schema(config):

	schema = Schema({
		'roles': [{
			'name': str,
			'model_set': str,
			'permission_set': str,
			Optional('users'): [str],
			Optional('groups'): [str]
		}],
		'groups': [{
			'name': str,
			Optional('users'): [str],
			Optional('groups'): [str]
		}],
		'model_sets': [{
			'name': str,
			'models': [str]
		}],
		'permission_sets': [{
			'name': str,
			'permissions': [str]
		}]
		})

	valid = schema.is_valid(config)

	if not valid:
		raise Exception("Your configuration's schema is not valid.")

def check_permission_sets(config, conn):

	permissions = conn.get_all_permissions()
	permission_names = [item['permission'] for item in permissions]

	for permission_set in config['permission_sets']:
		for permission in permission_set['permissions']:
			if permission not in permission_names:
				raise Exception('{} in permission set {} is not a valid permission.'.format(permission, permission_set['name']))

def check_model_sets(config, conn):

	models = conn.get_all_models()
	model_names = [item['name'] for item in models]

	for model_set in config['model_sets']:
		for model in model_set['models']:
			if model not in model_names:
				raise Exception('{} in model set {} is not a valid model.'.format(model, model_set['name']))

def check_groups_users(config, conn):

	users = conn.get_all_users()
	user_emails = [item['email'] for item in users if item['email']]

	for group in config['groups']:
		if 'users' in group:
			for user in group['users']:
				if user not in user_emails:
					raise Exception('User {} in group {} is not a valid user.'.format(user, group['name']))

def check_groups_groups(config, conn):

	group_names = [item['name'] for item in config['groups']]
	group_names.append('All Users')

	for group in config['groups']:
		if 'groups' in group:
			for subgroup in group['groups']:
				if subgroup not in group_names:
					raise Exception('Subgroup {} in group {} is not defined as a group in your configuration.'.format(subgroup, group['name']))

	dag = generate_groups_dag(config['groups'])

def check_roles_groups(config, conn):

	group_names = [item['name'] for item in config['groups']]
	group_names.append('All Users')

	for role in config['roles']:
		if 'groups' in role:
			for group in role['groups']:
				if group not in group_names:
					raise Exception('Group {} in role {} is not defined as a group in your configuration.'.format(group, role['name']))

def check_roles_users(config, conn):

	users = conn.get_all_users()
	user_emails = [item['email'] for item in users if item['email']]

	for role in config['roles']:
		if 'users' in role:
			for user in role['users']:
				if user not in user_emails:
					raise Exception('User {} in role {} is not a valid user.'.format(user, role['name']))

def check_roles_permission_sets(config, conn):

	permission_set_names = [item['name'] for item in config['permission_sets']]
	permission_set_names.append('Admin')

	for role in config['roles']:
			if role['permission_set'] not in permission_set_names:
				raise Exception('Permission set {} in role {} is not defined as a permission set in your configuration.'.format(role['permission_set'], role['name']))

def check_roles_model_sets(config, conn):

	model_set_names = [item['name'] for item in config['model_sets']]
	model_set_names.append('All')

	for role in config['roles']:
			if role['model_set'] not in model_set_names:
				raise Exception('Model set {} in role {} is not defined as a model set in your configuration.'.format(role['model_set'], role['name']))

def validate_config(config, conn):

	check_keys(config)
	check_schema(config)
	check_model_sets(config, conn)
	check_permission_sets(config, conn)
	check_groups_users(config, conn)
	check_groups_groups(config, conn)
	check_roles_groups(config, conn)
	check_roles_users(config, conn)
	check_roles_permission_sets(config, conn)
	check_roles_model_sets(config, conn)
