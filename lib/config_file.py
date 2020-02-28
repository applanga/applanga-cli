import click
from lib import constants
import os
import platform
import json


class ApplangaConfigFileNotValidException(Exception):
    pass


def getFilePath(current_folder=False):
    """Looks for a config file in current folder, APPLANGA_CONFIG and home directory and returns it.

    Args:
        current_folder: Returns only current folder path no matter if it exists or not.

    Returns:
        The converted language or None if conversion was not possible.

    """

    config_file_current_dir = os.path.join(os.getcwd(), constants.CONFIG_FILE_NAME)

    if current_folder is True or os.path.isfile(config_file_current_dir):
        return config_file_current_dir

    # Check if file exists under path of special environment variable
    if constants.ENVIRONMENT_VARIABLE in os.environ:
        applanga_config_path = os.environ[constants.ENVIRONMENT_VARIABLE]
        if applanga_config_path:
            file_path = os.path.join(applanga_config_path, constants.CONFIG_FILE_NAME)
            if os.path.isfile(file_path):
                return file_path

    # Check if file exists in home directory
    home_path = None
    if platform.system() == 'Windows':
        if 'HomePath' in os.environ:
            home_path = os.environ['HomePath']
    else:
        if 'HOME' in os.environ:
            home_path = os.environ['HOME']
    if home_path is not None:
        file_path = os.path.join(home_path, constants.CONFIG_FILE_NAME)
        if os.path.isfile(file_path):
            return file_path

    # If still no file got found that exists already, create under current path
    return config_file_current_dir



def write(data):
    """Writes config file in current directory.

    Args:
        data: Data to write in file.

    Returns:
        The config file path.

    """

    # Get the file path of config file. We write it always just in the current folder
    file_path = getFilePath(current_folder=True)

    with open(file_path, 'w') as outfile:
        click.echo('\nWrote the configuration to file: %s' % file_path)
        json_output = json.dumps(data, indent=2, sort_keys=True)
        click.echo('File content:')
        click.echo(json_output)
        json.dump(data, outfile, indent=2, sort_keys=True)

        return file_path


def readRaw():
    """Reads the config file and returns its information.

    Returns:
        The config file data.

    """

    try:
        file_path = getFilePath()
        with open(file_path, 'r') as stream:
            try:
                config_data = json.load(stream)

                # Make sure thae config file contains all the needed data
                if 'app' not in config_data:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have app data set.')
                
                env_access_token = os.environ.get('APPLANGA_ACCESS_TOKEN')
                if 'access_token' not in config_data['app']:
                    if env_access_token:
                        #click.echo('\nUsing access_token from enviroment var APPLANGA_ACCESS_TOKEN: %s' % env_access_token)
                        config_data['app']['access_token'] = env_access_token
                    else:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have an access token set.')

                if 'push' not in config_data['app']:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have push set.')
                if 'source' not in config_data['app']['push']:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source set.')
                if 1 > len(config_data['app']['push']['source']):
                    raise ApplangaConfigFileNotValidException('The config file is not valid. The source does not have any entry.')
                if 'path' not in config_data['app']['push']['source'][0]:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source path set under source.')
                if 'file_format' not in config_data['app']['push']['source'][0]:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source file_format set under source.')


                if 'pull' not in config_data['app']:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have pull set.')
                if 'target' not in config_data['app']['pull']:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target set.')
                if 1 > len(config_data['app']['pull']['target']):
                    raise ApplangaConfigFileNotValidException('The config file is not valid. The target does not have any entry.')
                if 'path' not in config_data['app']['pull']['target'][0]:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target path set under target.')
                if 'file_format' not in config_data['app']['pull']['target'][0]:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target file_format set under target.')

                return config_data

            except ValueError as e:
                raise ApplangaConfigFileNotValidException('The config file can not be parsed. Please fix or create a new one.')
    except IOError:
        raise ApplangaConfigFileNotValidException('The config file does not exist. Please initialize the project first with "applanga init"')


def read():
    """Reads the config file and returns its information. If none could be found it displays an error message.

    Returns:
        The config file data.

    """

    try:
        return readRaw()
    except ApplangaConfigFileNotValidException as e:
        click.secho(str(e), err=True, fg='red')
        return