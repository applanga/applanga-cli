import click
import os
import platform
from lib import api
from lib import config_file
from lib import constants
from lib import files
from lib import output

# Make sure that input works in Python 2 and 3
try:
   input = raw_input
except NameError:
   pass

@click.command()
@click.pass_context
@click.option('--access_token', help='access token of app')
@click.option('--file_format', help='the format of files (xml/strings)')
@click.option('--source_path', help='path to read files from')
@click.option('--target_path', help='path to writes files to')
@click.option('--force', type=click.BOOL, is_flag=True)
# @click.option('--count', default=1, help='number of greetings')
# @click.argument('name')

def init(ctx, access_token, file_format, source_path, target_path, force):
    output.showCommandHeader('init', ctx)

    config_file_path = config_file.getFilePath(current_folder=True)
    if os.path.isfile(config_file_path):
        if force != True:
            click.secho('Configuration file already exists at this location: %s' % config_file_path, err=True, fg='red')
            overwrite = input("To overwrite the file, type \"YES\": ")
            if overwrite == "YES":
                click.echo("File will be overwritten!\n")
            else:
                click.echo("File will not be overwritten so cancel!\n")
                return

    base_language = 'en'

    # Request all properties which are needed and did not get supplied
    # as arguments by user
    while not access_token:
        access_token = input('Access token: ')
        response_data = None

        # Make the request as simple and basic as possible
        data = {
                'includeDraft': 'false',
                'includeValue' : 'false',
                'includeSrc': 'false',
                'includeDescription' : 'false',
                'includeStatus' : 'false',
                'keepEmptyDataEntries' : 'false'
            }
        try:
            response = api.makeRequest(access_token=access_token, data=data, debug=ctx.obj['DEBUG'])
            response_data = response.json()
            click.echo('Access data got checked and is valid for app: "%s"\n' % response_data['name'])
            base_language = response_data['baseLanguage']
        except api.ApplangaRequestException as e:
            click.secho('There was a problem with supplied access token:\n%s\n' % str(e), err=True, fg='red')
            access_token = None

    while not file_format or file_format not in constants.FILE_FORMATS.keys():
        click.echo('\nChoose file format:')

        # Display a list of all the different available file formats
        counter = 0
        for key in constants.FILE_FORMATS.keys():
            counter += 1
            click.echo('[%d]\t%s\t\t%s' % (counter, constants.FILE_FORMATS[key]['name'], key))
        file_format_number = input('File format [%d-%d]: ' % (1, len(constants.FILE_FORMATS)))

        # Make sure that the selection is a number
        try:
            file_format_number = int(file_format_number)
        except:
            file_format_number = 0

        # Check if the selection is valid
        if file_format_number < 1 or file_format_number > len(constants.FILE_FORMATS):
            click.secho('The value "%s" is not valid. A a valid value is a number between 1 and %d.' % ( file_format_number, len(constants.FILE_FORMATS)), err=True, fg='red')
        else:
            file_format = list(constants.FILE_FORMATS.keys())[file_format_number-1]
            click.echo('You selected: %s\n' % file_format)

    if not source_path:

        default_source_path = constants.FILE_FORMATS[file_format]['default_file_path']
        if platform.system() == 'Windows':
            # If we are in Windows convert into correct format
            default_source_path = files.convertToWindowsPath(default_source_path)

        source_path = input('Source path [\"%s\"]: ' % default_source_path)
        source_path = source_path or default_source_path
    if not target_path:
        target_path = input('Target path [\"%s\"]: ' % source_path)
        target_path = target_path or source_path

    # Save the configuration file
    configfile_data = {
        'app': {
            'access_token': access_token,
            'base_language': base_language,
            'push': {
                'source': [
                    {
                        'file_format': file_format,
                        'path': source_path
                    }
                ]
            },
            'pull': {
                'target': [
                    {
                        'file_format': file_format,
                        'path': target_path
                    }
                ]
            }
        }
    }

    # Write the new config file to local folder
    config_file.write(configfile_data)