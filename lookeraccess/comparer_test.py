from lookeraccess.comparer import find_items_to_update, find_sublist_items_to_remove, find_sublist_items_to_add

def test_find_items_to_update_role_permission_set_no_change():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	assert find_items_to_update(looker_config, new_config, 'roles', 'name', 'permission_set') == []

def test_find_items_to_update_role_users_no_change():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	assert find_items_to_update(looker_config, new_config, 'roles', 'name', 'users', True) == []

def test_find_sublist_items_to_remove_role_users_no_change():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	assert find_sublist_items_to_remove(looker_config, new_config, 'roles', 'name', 'users') == []

def test_find_sublist_items_to_remove_role_users_changed():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com'
			]
			}
		]
	}

	changes = find_sublist_items_to_remove(looker_config, new_config, 'roles', 'name', 'users')
	print(changes)

	assert changes == [{'name': 'second_role', 'item': ['stephen@geller.com']}]

def test_find_sublist_items_to_remove_role_users_removed():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone'
			}
		]
	}

	changes = find_sublist_items_to_remove(looker_config, new_config, 'roles', 'name', 'users')
	print(changes)

	assert changes == [{'name': 'second_role', 'item': ['dylan@baker.com','stephen@geller.com']}]

def test_find_sublist_items_to_add_role_users_changed():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com'
			]
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	changes = find_sublist_items_to_add(looker_config, new_config, 'roles', 'name', 'users')
	print(changes)

	assert changes == [{'name': 'second_role', 'item': ['stephen@geller.com']}]

def test_find_sublist_items_to_add_role_users_added():

	looker_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone'
			}
		]
	}

	new_config = {
		'roles': [{
			'name': 'first_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			},
			{
			'name': 'second_role',
			'model_set': 'msone',
			'permission_set': 'psone',
			'users' :[
				'dylan@baker.com',
				'stephen@geller.com'
			]
			}
		]
	}

	changes = find_sublist_items_to_add(looker_config, new_config, 'roles', 'name', 'users')
	print(changes)

	assert changes == [{'name': 'second_role', 'item': ['dylan@baker.com','stephen@geller.com']}]
