import click
import requests
from lib import api
from lib import config_file
from lib import output


@click.command()
@click.pass_context
def pull(ctx):
    output.showCommandHeader('pull', ctx)

    try:
        config_file_data = config_file.readRaw()
    except config_file.ApplangaConfigFileNotValidException as e:
        click.secho('There was a problem with the config file:\n%s\n' % str(e), err=True, fg='red')
        return

    all_app_languages = []
    for target in config_file_data['app']['pull']['target']:
        if 'language' not in target:
            if '<language>' not in target['path']:
                # If also no placeholder is defined then there is no need to
                # query languages from API
                continue

            try:
                all_app_languages = api.getAllAppLanguages(debug=ctx.obj['DEBUG'])
            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem getting the app languages:\n%s\n' % str(e), err=True, fg='red')
                return

            break


    request_languages = []
    for target in config_file_data['app']['pull']['target']:

        if 'language' in target:
            # Language is defined in config
            request_languages = [ target['language'] ]
        elif '<language>' in target['path']:
            # Language laceholder is defined in path so download all languages
            request_languages = all_app_languages
        else:
            # No language defined so error
            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], 'missing'))
            click.echo('=' * 60)
            click.echo('Result: "Error"')
            click.secho('No language defined. It either has to be set as property or as placeholder in path.\n', err=True, fg='red')
            continue

        # Go through all the languages that should be downloaded
        for language in request_languages:
            target['language'] = language

            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], language))
            click.echo('=' * 60)

            try:
                file_written = api.downloadFile(target, debug=ctx.obj['DEBUG'])
                click.echo('Result: "Success"')
                click.echo('Wrote file: %s' % file_written)

            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem with downloading file:\n%s\n' % str(e), err=True, fg='red')
                return
