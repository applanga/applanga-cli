#!/usr/bin/env python

import click
from lib import constants
import commands

@click.group()
@click.version_option('1.0.26')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug


# Add all the commands we support
cli.add_command(commands.config.config)
cli.add_command(commands.init.init)
cli.add_command(commands.pull.pull)
cli.add_command(commands.push.push)

# Initialize the command line tool
if __name__ == '__main__':
    cli(obj={})