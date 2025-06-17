import click
import requests
from lib import api
from lib import config_file
from lib import output

@click.command()
@click.pass_context
@click.option('--force', type=click.BOOL, is_flag=True, help="Overwrite existing values")
@click.option('--draft', type=click.BOOL, is_flag=True, help="Upload values as draft")
def pushTarget(ctx, force, draft):
    output.showCommandHeader('push', ctx)

    try:
        config_file_data = config_file.readRaw()

        if 'pull' not in config_file_data['app']:
            click.echo('In order to Push target you need to have a pull configuration set in your config file')
            return
    except config_file.ApplangaConfigFileNotValidException as e:
        click.secho('There was a problem with the config file:\n%s\n' % str(e), err=True, fg='red')
        return


    try:
        file_responses = api.uploadFiles(ctx, config_file_data['app']['pull']['target'], force=force, draft=draft)
    except api.ApplangaRequestException as e:
        click.secho('There was a problem with pushing files:\n%s\n' % str(e), err=True, fg='red')
        return

    if len(file_responses) == 0:
        click.secho('No file to upload got found.', err=True, fg='red')

    for upload_data in file_responses:
        language = upload_data['language'] if 'language' in upload_data else 'language missing'
        click.echo('\nUpload   :  %s\nLanguage :  %s' % (upload_data['path'], language))
        click.echo('=' * 60)

        if 'error' in upload_data:
            # There was a problem with the import
            click.echo('Result: "Error"')
            click.secho('There was a problem with importing file:\n%s\n' % upload_data['error'], err=True, fg='red')
            continue

        # Import was successful
        response_json = upload_data['response'].json()
        click.echo('Result: "Success"\n\n - Entries in file: %d\n - Added:           %d\n - Updated:         %d\n - Tag updates:     %d\n' % (response_json['total'], response_json['added'], response_json['updated'], response_json['tagUpdates']))
