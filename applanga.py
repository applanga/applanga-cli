#!/usr/bin/env python

import click
from lib import constants
import commands

@click.group()
@click.version_option(constants.VERSION_NUMBER)
@click.option('--debug/--no-debug', default=False)
@click.option('--disable-cert-verification', default=False, is_flag=True)
@click.pass_context
def cli(ctx, debug, disable_cert_verification):
    ctx.obj['DEBUG'] = debug
    ctx.obj['disable-cert-verification'] = disable_cert_verification


# Add all the commands we support
cli.add_command(commands.config.config)
cli.add_command(commands.init.init)
cli.add_command(commands.pull.pull)
cli.add_command(commands.push.push)
cli.add_command(commands.updateSettingsfiles.updateSettingsfiles)
cli.add_command(commands.pullSource.pullSource)
cli.add_command(commands.pushTarget.pushTarget)

# Initialize the command line tool
if __name__ == '__main__':
    cli(obj={})
