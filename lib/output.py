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


def abort_if_fail_on_error(ctx, fail_on_error, message=None):
    """Abort execution with exit code 1 if fail_on_error is set."""
    if not fail_on_error:
        return

    if message:
        click.secho(message, err=True, fg='red')
    ctx.exit(1)