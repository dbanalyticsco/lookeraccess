import pytest
from lookeraccess.utils import compose_url

BASE_URL = 'https://test_url.looker.com:19999/api/3.0/'

def test_compose_url_endpoint():

	assert compose_url(BASE_URL, 'projects') == 'https://test_url.looker.com:19999/api/3.0/projects'

def test_compose_url_endpointid():

	assert compose_url(BASE_URL, 'projects', 'looker_project') == 'https://test_url.looker.com:19999/api/3.0/projects/looker_project'

def test_compose_url_subendpoint():

	assert compose_url(BASE_URL, 'projects', 'looker_project', 'git_branches') == 'https://test_url.looker.com:19999/api/3.0/projects/looker_project/git_branches'

def test_compose_url_subendpoint():

	assert compose_url(BASE_URL, 'projects', 'looker_project', 'git_branches', 'hotfix_2') == 'https://test_url.looker.com:19999/api/3.0/projects/looker_project/git_branches/hotfix_2'

def test_compose_url_no_endpoint():

	with pytest.raises(Exception):
		compose_url(BASE_URL)

def test_compose_url_no_url():

	with pytest.raises(Exception):
		compose_url(endpoint='projects')