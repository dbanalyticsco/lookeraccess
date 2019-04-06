import click
from connection import LookerConnection
from utils import compose_url

@click.group()
def cli():
	pass

@click.command()
def hello():
	click.echo('Hello. This is a test.')

@click.command()
@click.argument('base_url')
@click.argument('client_id')
@click.argument('client_secret')
def connect(base_url, client_id, client_secret):
	
	conn = LookerConnection(client_id, client_secret, base_url)

	if conn.headers:
		click.echo('Successfully connected to Looker instance: {}'.format(base_url))
	else:
		click.echo('Unable to connect to Looker instance: {}'.format(base_url))


@click.command()
@click.argument('base_url')
@click.argument('client_id')
@click.argument('client_secret')
def pull(base_url, client_id, client_secret):
	
	conn = LookerConnection(client_id, client_secret, base_url)

	if conn.headers:
		click.echo('Successfully connected to Looker instance: {}'.format(base_url))
	else:
		click.echo('Unable to connect to Looker instance: {}'.format(base_url))
	
	click.echo(conn.get_model_sets())	
	click.echo(conn.get_permission_sets())	
	click.echo(conn.get_roles())	
	click.echo(conn.get_role_users(2))
	click.echo(conn.get_role_groups(8))


cli.add_command(hello)
cli.add_command(connect)
cli.add_command(pull)

if __name__ == '__main__':
	cli()