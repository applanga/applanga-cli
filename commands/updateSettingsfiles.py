import click
import requests
from lib import api, constants
from lib import output
import os
import tarfile
import json
from lib import api


@click.command('updateSettingsfiles')
@click.pass_context
def updateSettingsfiles(ctx):
    output.showCommandHeader('updateSettingsfiles', ctx)

    projectPath = os.getcwd()

    click.echo('-> searching for applanga settingfiles in ' + projectPath)

    for root, dirs, files in os.walk(projectPath):
        for file in files:
            if file.endswith('.applanga'):
                try:
                    path = os.path.join(root, file)
                    click.echo("--> found: '%s' in '%s'" %
                               (file, path[len(os.getcwd())+1: len(path)]))
                    tar = tarfile.open(path)
                    alData = json.load(tar.extractfile(
                        tar.getmember('app.applanga')))
                    appId = alData['_id']
                    apiSecret = alData['apiSecret']
                    lastVersion = alData['__v']
                    if not 'groupIds' in alData.keys():
                        click.echo(
                            'Error: Your settingsfile is to old please update manually once before using the auto update script.')
                        continue
                    groupIds = alData['groupIds']
                except (Exception):
                    click.secho('Settingsfile parsing error')
                else:
                    try:
                        url = "/projects/%s/updateSettings" % (appId)

                        responseJson = api.makeRequest(api_path=url, data={
                                                       'groupIds': groupIds, 'apiSecret': apiSecret, 'lastVersion': lastVersion}, base_path='/v1').json()

                        if responseJson['update'] == True:
                            downloadSettingsFile(responseJson['settings'], path)
                            click.echo('---> Settingsfile updated!')
                        else:
                            click.echo('---> Settingsfile up-to-date')
                        tar.close()
                    except Exception as e:
                        click.secho('Settingsfile update error:\n%s\n' %str(e), err=True, fg='red')


def downloadSettingsFile(url, path):
    """Downloads a settings file from given url

    Args:
        url: Absolute url to the settings file
        path: Path to existing settings file that will be overwritten by download

    Returns:
        None
    """
    try:
        response = requests.get(url)
        open(path, 'wb').write(response.content)
    except requests.exceptions.ConnectionError as e:
        raise api.ApplangaRequestException('Problem connecting to server. Please check your internet connection.')
    except:
        raise Exception('Unknown error occured.')
