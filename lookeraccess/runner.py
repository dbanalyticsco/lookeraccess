from lookeraccess.utils import generate_groups_dag
import networkx as nx

def change_permission_sets(conn, looker_config, new_config, changes):

	for item in changes['delete']:
		item_id = next((e for e in looker_config if e['name'] == item))['id']
		conn.delete_permission_set(item_id)

	for item in changes['create']:
		item_to_create = next((e for e in new_config if e['name'] == item))
		conn.create_permission_set(item_to_create['name'], item_to_create['permissions'])

	for item in changes['update']:
		update_item_id = next((e for e in looker_config if e['name'] == item))['id']
		item_to_update = next((e for e in new_config if e['name'] == item))
		conn.update_permission_set(update_item_id, item_to_update['name'], item_to_update['permissions'])

def change_model_sets(conn, looker_config, new_config, changes):

	for item in changes['delete']:
		item_id = next((e for e in looker_config if e['name'] == item))['id']
		conn.delete_model_set(item_id)

	for item in changes['create']:
		item_to_create = next((e for e in new_config if e['name'] == item))
		conn.create_model_set(item_to_create['name'], item_to_create['models'])

	for item in changes['update']:
		update_item_id = next((e for e in looker_config if e['name'] == item))['id']
		item_to_update = next((e for e in new_config if e['name'] == item))
		conn.update_model_set(update_item_id, item_to_update['name'], item_to_update['models'])

def change_groups(conn, looker_config, new_config, changes):

	# Delete
	for item in changes['delete']:
		item_id = next((e for e in looker_config if e['name'] == item))['id']
		conn.delete_group(item_id)

	# Create
	dag = generate_groups_dag(new_config)
	users = conn.get_all_users()

	for item in nx.topological_sort(dag):

		if item in changes['create']:
			item_to_create = next((e for e in new_config if e['name'] == item))
			
			created_group = conn.create_group(item_to_create['name'])
			created_item_id = created_group['id']
			
			groups = conn.get_groups()

			if 'groups' in item_to_create:
				for subitem in item_to_create['groups']:
					subitem_id = next((e for e in groups if e['name'] == subitem))['id']
					conn.add_group_to_group(created_item_id, subitem_id)

			if 'users' in item_to_create:
				for subitem in item_to_create['users']:
					subitem_id = next((e for e in users if e['email'] == subitem))['id']
					conn.add_user_to_group(created_item_id, subitem_id)

	# Update
	groups = conn.get_groups()		

	for item in changes['update']['groups']['add']:
		update_item_id = next((e for e in looker_config if e['name'] == item['name']))['id']
		for group in item['item']:
			subitem_id = next((e for e in groups if e['name'] == group))['id']
			conn.add_group_to_group(update_item_id, subitem_id)

	for item in changes['update']['groups']['remove']:
		update_item_id = next((e for e in looker_config if e['name'] == item['name']))['id']
		for group in item['item']:
			subitem_id = next((e for e in groups if e['name'] == group))['id']
			conn.remove_group_from_group(update_item_id, subitem_id)

	for item in changes['update']['users']['add']:
		update_item_id = next((e for e in looker_config if e['name'] == item['name']))['id']
		for user in item['item']:
			subitem_id = next((e for e in users if e['email'] == user))['id']
			conn.add_user_to_group(update_item_id, subitem_id)

	for item in changes['update']['users']['remove']:
		update_item_id = next((e for e in looker_config if e['name'] == item['name']))['id']
		for user in item['item']:
			subitem_id = next((e for e in users if e['email'] == user))['id']
			conn.remove_user_from_group(update_item_id, subitem_id)

def change_roles(conn, looker_config, new_config, changes):
	
	groups = conn.get_groups()	
	users = conn.get_all_users()
	permission_sets = conn.get_permission_sets()
	model_sets = conn.get_model_sets()

	# Delete
	for item in changes['delete']:
		item_id = next((e for e in looker_config if e['name'] == item))['id']
		conn.delete_role(item_id)

	# Create
	for item in changes['create']:
		item_to_create = next((e for e in new_config if e['name'] == item))
		permission_set_id = next((e for e in permission_sets if e['name'] == item_to_create['permission_set']))['id']
		model_set_id = next((e for e in model_sets if e['name'] == item_to_create['model_set']))['id']
		
		created_role = conn.create_role(item_to_create['name'], permission_set_id, model_set_id)
		created_role_id = created_role['id']

		if 'groups' in item_to_create:
			role_groups = []
			for group in item_to_create['groups']:
				group_id = next((e for e in groups if e['name'] == group))['id']
				role_groups.append(group_id)
			conn.update_role_groups(created_role_id, role_groups)

		if 'users' in item_to_create:
			role_users = []
			for user in item_to_create['users']:
				user_id = next((e for e in users if e['email'] == user))['id']
				role_users.append(user_id)
			conn.update_role_users(created_role_id, role_users)

	# Update
	for item in changes['update']:
		update_item_id = next((e for e in looker_config if e['name'] == item['name']))['id']
		item_to_update = next((e for e in new_config if e['name'] == item['name']))
		permission_set_id = next((e for e in permission_sets if e['name'] == item_to_update['permission_set']))['id']
		model_set_id = next((e for e in model_sets if e['name'] == item_to_update['model_set']))['id']
		
		if item['role']:
			conn.update_role(update_item_id, item_to_update['name'], permission_set_id, model_set_id)
		
		if item['groups']:

			role_groups = []
			if 'groups' in item_to_update:
				for group in item_to_update['groups']:
					group_id = next((e for e in groups if e['name'] == group))['id']
					role_groups.append(group_id)
			conn.update_role_groups(update_item_id, role_groups)
		
		if item['users']: 
			role_users = []
			if 'users' in item_to_update:
				for user in item_to_update['users']:
					user_id = next((e for e in users if e['email'] == user))['id']
					role_users.append(user_id)
			conn.update_role_users(update_item_id, role_users)

def implement_changes(conn, looker_config, new_config, changes):
	
	change_permission_sets(conn, looker_config['permission_sets'], new_config['permission_sets'], changes['permission_sets'])
	change_model_sets(conn, looker_config['model_sets'], new_config['model_sets'], changes['model_sets'])
	change_groups(conn, looker_config['groups'], new_config['groups'], changes['groups'])
	change_roles(conn, looker_config['roles'], new_config['roles'], changes['roles'])
