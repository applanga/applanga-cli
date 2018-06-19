import click
import json
from lib import config_file
from lib import output


@click.command()
@click.pass_context
def config(ctx):
    output.showCommandHeader('config', ctx)

    # Check if a config file exists
    config_file_data = config_file.read()
    if not config_file_data:
        click.echo('No config file found')
        return

    # Config file exists. So get path and content to display it to user
    config_path = config_file.getFilePath()
    click.echo('Found following config file:\n%s\n\nContent: ' % config_path)

    json_output = json.dumps(config_file_data, indent=2, sort_keys=True)
    click.echo(json_output)
