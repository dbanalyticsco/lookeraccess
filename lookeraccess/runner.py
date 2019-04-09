

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

def implement_changes(conn, looker_config, new_config, changes):
	
	change_permission_sets(conn, looker_config['permission_sets'], new_config['permission_sets'], changes['permission_sets'])
	change_model_sets(conn, looker_config['model_sets'], new_config['model_sets'], changes['model_sets'])
