import click
from connection import LookerConnection
from utils import compose_url
from parser import log_looker_config_file
from loader import load_config_files
from validator import validate_config

@click.group()
def cli():
	pass

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
def connect(base_url, client_id, client_secret):
	
	conn = LookerConnection(client_id, client_secret, base_url)

	if conn.headers:
		click.echo('Successfully connected to Looker instance: {}'.format(base_url))
	else:
		click.echo('Unable to connect to Looker instance: {}'.format(base_url))


@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
def pull(base_url, client_id, client_secret):
	
	conn = LookerConnection(client_id, client_secret, base_url)

	if conn.headers:
		click.echo('Successfully connected to Looker instance: {}'.format(base_url))
	else:
		click.echo('Unable to connect to Looker instance: {}'.format(base_url))

	log_looker_config_file(conn, pull=True)

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
def validate(base_url, client_id, client_secret):
	
	conn = LookerConnection(client_id, client_secret, base_url)
	config = load_config_files()
	validate_config(config, conn)

cli.add_command(connect)
cli.add_command(pull)
cli.add_command(validate)

if __name__ == '__main__':
	cli()