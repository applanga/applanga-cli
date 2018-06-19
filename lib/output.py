import click

def showCommandHeader(command_name, ctx):
    """Displays basic information to user.

    Args:
        command_name: The name of the command which started method.

    Returns:
        Noting

    """
    if ctx.obj['DEBUG']:
        click.echo('')
        click.echo('*' * 60)
        click.echo('Executing command: %s' % command_name)
        click.echo('*' * 60)

        click.echo('Debug Mode is %s' % (ctx.obj['DEBUG'] and 'activated' or 'deactivated'))