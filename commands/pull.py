import click
import requests
from lib import api
from lib import config_file
from lib import output
from lib import options
import json


@click.command()
@click.pass_context
@click.option(
    '--tag',
    'tags',
    multiple=True,
    help='Only pull entries with the specified tags. Can be specified multiple times, e.g. --tag login --tag error'
)

def pull(ctx, tags):
    output.showCommandHeader('pull', ctx)

    is_valid, parsed_tags = options.parse_and_validate_tags(tags)
    if not is_valid:
        return

    try:
        config_file_data = config_file.readRaw()

        if 'pull' not in config_file_data['app']:
            click.echo('In order to Pull you need to have a pull configuration set in your config file')
            return
    except config_file.ApplangaConfigFileNotValidException as e:
        click.secho('There was a problem with the config file:\n%s\n' % str(e), err=True, fg='red')
        return
    
    options.log_config(ctx, config_file_data)

    try: 
        projectVersion = api.getProjectVersion(ctx)
    except api.ApplangaConnectionException as e:
        click.secho(str(e), err=True, fg='red')
        return
    except api.ApplangaRequestException as e:
        click.echo(str(e))
        return
    
    all_app_languages = []
    for target in config_file_data['app']['pull']['target']:
        if 'language' not in target:
            if '<language>' not in target['path']:
                # If also no placeholder is defined then there is no need to
                # query languages from API
                continue

            try:
                all_app_languages = api.getAllAppLanguages(ctx, projectVersion)
            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem getting the app languages:\n%s\n' % str(e), err=True, fg='red')
                return

            break

    request_languages = []

    target_files = config_file_data['app']['pull']['target']

    # Filter if parsed_tags is set
    if parsed_tags:
        try:
            target_files = options.filter_files_by_tags(target_files, parsed_tags)
        except Exception as e:
            click.secho('There was a problem while filtering target files by tags:\n%s\n' % str(e), err=True, fg='red')
            return
    else:
        # check 400 chars limit for tag names
        if not options.validate_tags_length_in_files(target_files):
            return

    for target in target_files:

        if 'language' in target:
            # Language is defined in config
            request_languages = [ target['language'] ]
        elif '<language>' in target['path']:
            # Language placeholder is defined in path so download all languages
            request_languages = list(all_app_languages)
        else:
            # No language defined so error
            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], 'missing'))
            click.echo('=' * 60)
            click.echo('Result: "Error"')
            click.secho('You either need to use the <language> wildcard inside the path string or set it explicitly per file via the "language" property. \nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.\n', err=True, fg='red')
            continue


        # Remove all the languages on the exclude list
        exclude_languages = []
        if 'exclude_languages' in target:
            exclude_languages = target['exclude_languages']

        request_languages = [x for x in request_languages if x not in exclude_languages]

        target['projectVersion'] = projectVersion
        
        # Go through all the languages that should be downloaded
        for language in request_languages:
            target['language'] = language

            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], language))
            click.echo('=' * 60)

            try:
                file_written = api.downloadFile(ctx, target)
                click.echo('Result: "Success"')
                click.echo('Wrote file: %s' % file_written)

            except api.ApplangaConnectionException as e:
                click.secho(str(e), err=True, fg='red')
                return

            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem with downloading file:\n%s\n' % str(e), err=True, fg='red')
                if str(e).startswith('API response: Error: Tag with name'):
                    click.echo('You might need to push your content in order to have the Tag created first')
                return
