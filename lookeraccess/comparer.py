# ABSTRACT

def find_items_to_delete(looker_config, new_config, item_type, identifier):

	new_names = [item[identifier] for item in new_config[item_type]]
	items_to_delete = []

	for item in looker_config[item_type]:
		if item[identifier] not in new_names:
			items_to_delete.append(item[identifier])

	return items_to_delete

def find_items_to_create(looker_config, new_config, item_type, identifier):

	names = [item[identifier] for item in looker_config[item_type]]
	items_to_create = []

	for item in new_config[item_type]:
		if item[identifier] not in names:
			items_to_create.append(item[identifier])

	return items_to_create

def find_items_to_update(looker_config, new_config, item_type, identifier, subitem, is_list=False):

	new_names = [item[identifier] for item in new_config[item_type]]
	items_to_update = []

	for item in looker_config[item_type]:
		if item[identifier] in new_names:
			new_item = next((e for e in new_config[item_type] if e[identifier] == item[identifier]))

			if is_list:
				
				if (subitem in new_item and subitem not in item) or (subitem not in new_item and subitem in item):
					items_to_update.append(item[identifier])
				
				elif subitem in new_item and subitem in item:
					new_item[subitem].sort()
					item[subitem].sort()
					print('{} / {}'.format(item[identifier], subitem))
					print(new_item[subitem])
					print(item[subitem])
					if new_item[subitem] != item[subitem]:
						items_to_update.append(item[identifier])
			
			else:
				if new_item[subitem] != item[subitem]:
					items_to_update.append(item[identifier])


	return items_to_update

def find_sublist_items_to_add():
	pass

def find_sublist_items_to_remove():
	pass

# PERMISSION SETS

def find_permission_sets_to_delete(looker_config, new_config):

	return find_items_to_delete(looker_config, new_config, 'permission_sets', 'name')

def find_permission_sets_to_create(looker_config, new_config):

	return find_items_to_create(looker_config, new_config, 'permission_sets', 'name')

def find_permission_sets_to_update(looker_config, new_config):

	return find_items_to_update(looker_config, new_config, 'permission_sets', 'name', 'permissions', True)

def find_permission_set_changes(looker_config, new_config):

	changes = {}
	changes['delete'] = find_permission_sets_to_delete(looker_config, new_config)
	changes['update'] = find_permission_sets_to_update(looker_config, new_config)
	changes['create'] = find_permission_sets_to_create(looker_config, new_config)

	return changes

# MODEL SETS

def find_model_sets_to_delete(looker_config, new_config):

	return find_items_to_delete(looker_config, new_config, 'model_sets', 'name')

def find_model_sets_to_create(looker_config, new_config):

	return find_items_to_create(looker_config, new_config, 'model_sets', 'name')

def find_model_sets_to_update(looker_config, new_config):

	return find_items_to_update(looker_config, new_config, 'model_sets', 'name', 'models', True)

def find_model_set_changes(looker_config, new_config):

	changes = {}
	changes['delete'] = find_model_sets_to_delete(looker_config, new_config)
	changes['update'] = find_model_sets_to_update(looker_config, new_config)
	changes['create'] = find_model_sets_to_create(looker_config, new_config)

	return changes

# GROUPS

def find_groups_to_delete(looker_config, new_config):

	return find_items_to_delete(looker_config, new_config, 'groups', 'name')

def find_groups_to_create(looker_config, new_config):

	return find_items_to_create(looker_config, new_config, 'groups', 'name')

def find_groups_to_update(looker_config, new_config):

	pass

def find_group_changes(looker_config, new_config):

	changes = {}
	changes['delete'] = find_groups_to_delete(looker_config, new_config)
	# changes['update'] = find_groups_to_update(looker_config, new_config)
	changes['create'] = find_groups_to_create(looker_config, new_config)

	return changes

# ROLES

def find_roles_to_delete(looker_config, new_config):

	return find_items_to_delete(looker_config, new_config, 'roles', 'name')

def find_roles_to_create(looker_config, new_config):

	return find_items_to_create(looker_config, new_config, 'roles', 'name')

def find_roles_to_update(looker_config, new_config):

	users = find_items_to_update(looker_config, new_config, 'roles', 'name', 'users', True)
	groups = find_items_to_update(looker_config, new_config, 'roles', 'name', 'groups', True)
	model_sets = find_items_to_update(looker_config, new_config, 'roles', 'name', 'model_set')
	permission_sets = find_items_to_update(looker_config, new_config, 'roles', 'name', 'permission_set')

	roles = users + groups + model_sets + permission_sets
	roles = list(dict.fromkeys(roles))

	update_list = []

	for role in roles:
		item = {
			'name': role,
			'users': role in users,
			'groups': role in groups,
			'role': role in model_sets or role in permission_sets
		}
		update_list.append(item)

	return update_list

def find_role_changes(looker_config, new_config):

	changes = {}
	changes['delete'] = find_roles_to_delete(looker_config, new_config)
	changes['update'] = find_roles_to_update(looker_config, new_config)
	changes['create'] = find_roles_to_create(looker_config, new_config)

	return changes

def find_changes(looker_config, new_config):

	changes = {}
	# changes['permission_sets'] = find_permission_set_changes(looker_config, new_config)
	# changes['model_sets'] = find_model_set_changes(looker_config, new_config)
	# changes['groups'] = find_group_changes(looker_config, new_config)
	changes['roles'] = find_role_changes(looker_config, new_config)
	
	return changes

