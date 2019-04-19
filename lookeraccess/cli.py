import click
from lookeraccess.connection import LookerConnection
from lookeraccess.utils import compose_url
from lookeraccess.parser import log_looker_config_file, log_raw_looker_config_file, clean_looker_config, get_looker_config, load_looker_config_from_logs
from lookeraccess.loader import load_config_files
from lookeraccess.validator import validate_config
from lookeraccess.comparer import find_changes
from lookeraccess.runner import implement_changes
from datetime import datetime

@click.group()
def cli():
	pass

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
@click.option('--port', default=19999)
def connect(base_url, client_id, client_secret, port):
	
	conn = LookerConnection(client_id, client_secret, base_url, port)

	if conn.headers:
		click.echo('Successfully connected to Looker instance: {}'.format(base_url))
	else:
		click.echo('Unable to connect to Looker instance: {}'.format(base_url))


@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
@click.option('--port', default=19999)
def pull(base_url, client_id, client_secret, port):

	run_time = datetime.now()
	conn = LookerConnection(client_id, client_secret, base_url, port)
	looker_config_raw = get_looker_config(conn)
	log_raw_looker_config_file(conn, looker_config_raw, run_time)
	looker_config = clean_looker_config(looker_config_raw)
	log_looker_config_file(conn, looker_config, run_time, pull=True)

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
@click.option('--port', default=19999)
def validate(base_url, client_id, client_secret, port):
	
	conn = LookerConnection(client_id, client_secret, base_url, port)
	config = load_config_files()
	validate_config(config, conn)

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
@click.option('--port', default=19999)
@click.option('--uselog', is_flag=True)
def changes(base_url, client_id, client_secret, uselog, port):

	run_time = datetime.now()
	conn = LookerConnection(client_id, client_secret, base_url, port)
	new_config = load_config_files()
	validate_config(new_config, conn)
	if uselog:
		looker_config_raw = load_looker_config_from_logs()
	else:
		looker_config_raw = get_looker_config(conn)
	log_raw_looker_config_file(conn, looker_config_raw, run_time)
	looker_config = clean_looker_config(looker_config_raw)
	log_looker_config_file(conn, looker_config, run_time)
	click.echo(find_changes(looker_config, new_config))

@click.command()
@click.argument('base_url', envvar='LOOKER_BASE_URL')
@click.argument('client_id', envvar='LOOKER_CLIENT_ID')
@click.argument('client_secret', envvar='LOOKER_CLIENT_SECRET')
@click.option('--port', default=19999)
@click.option('--uselog', is_flag=True)
def run(base_url, client_id, client_secret, uselog, port):

	run_time = datetime.now()
	conn = LookerConnection(client_id, client_secret, base_url, port)
	new_config = load_config_files()
	if uselog:
		looker_config_raw = load_looker_config_from_logs()
	else:
		looker_config_raw = get_looker_config(conn)
	log_raw_looker_config_file(conn, looker_config_raw, run_time)
	looker_config = clean_looker_config(looker_config_raw)
	log_looker_config_file(conn, looker_config, run_time)
	changes = find_changes(looker_config, new_config)
	looker_config_raw = load_looker_config_from_logs()
	implement_changes(conn, looker_config_raw, new_config, changes)

cli.add_command(connect)
cli.add_command(pull)
cli.add_command(validate)
cli.add_command(changes)
cli.add_command(run)

if __name__ == '__main__':
	cli()