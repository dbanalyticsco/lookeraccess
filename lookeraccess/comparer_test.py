from lookeraccess.comparer import find_items_to_update

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