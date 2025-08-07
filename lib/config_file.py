import click
from lib import constants
import os
import platform
import json
from functools import cmp_to_key
from pathlib import Path


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

                if 'push' not in config_data['app'] and 'pull' not in config_data['app']:
                    raise ApplangaConfigFileNotValidException('The config file is not valid. Either a push or pull block has to be set')

                if 'push' in config_data['app']:
                    if 'source' not in config_data['app']['push']:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source set.')
                    if 1 > len(config_data['app']['push']['source']):
                        raise ApplangaConfigFileNotValidException('The config file is not valid. The source does not have any entry.')
                    if 'path' not in config_data['app']['push']['source'][0]:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source path set under source.')
                    if 'file_format' not in config_data['app']['push']['source'][0]:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have source file_format set under source.')

                if 'pull' in config_data['app']:
                    if 'target' not in config_data['app']['pull']:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target set.')
                    if 1 > len(config_data['app']['pull']['target']):
                        raise ApplangaConfigFileNotValidException('The config file is not valid. The target does not have any entry.')
                    if 'path' not in config_data['app']['pull']['target'][0]:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target path set under target.')
                    if 'file_format' not in config_data['app']['pull']['target'][0]:
                        raise ApplangaConfigFileNotValidException('The config file is not valid. It does not have target file_format set under target.')

                testTagConflict(config_data)
                
                return config_data

            except ValueError as e:
                raise ApplangaConfigFileNotValidException('The config file can not be parsed. Please fix or create a new one.')
    except IOError:
        raise ApplangaConfigFileNotValidException('The config file does not exist. Please initialize the project first with "applanga init"')


#Utiliti claas used to see if a cli target / source block is tackling the same language/path/tag together
class FileBlock:
    def __init__(self, fileBlockData):
        self.language = None
        if 'language' in fileBlockData:
            self.language = fileBlockData['language']

        self.tag = None
        if 'tag' in fileBlockData:
            self.tag = fileBlockData['tag']
            
        self.path = ''
        if 'path' in fileBlockData:
            self.path = fileBlockData['path']

        self.exclude_languages = []
        if 'exclude_languages' in fileBlockData:
            self.exclude_languages = fileBlockData['exclude_languages']

        self.file_format = None
        if 'file_format' in fileBlockData:
            self.file_format = fileBlockData['file_format']
        
        self.tag_category = None
        if 'tag_category' in fileBlockData:
            self.tag_category = fileBlockData['tag_category']

    def compareTag(self, other): 
        tagEqual = None
        if isinstance(self.tag, list):
            if isinstance(other.tag, list):
                overlap = set(self.tag) & set(other.tag)
                if overlap:
                    tagEqual = list(overlap)[0]
            elif other.tag in self.tag:
                tagEqual = other.tag
        else:
            if isinstance(other.tag, list) and self.tag in other.tag:
                tagEqual = self.tag
            elif self.tag == other.tag:
                tagEqual = self.tag
        return tagEqual

    def ignoreFormatOverlap(self, other):
        if Path(self.path).stem != Path(other.path).stem:
            return False
        for exclude in constants.EXCLUDE_FORMAT_OVERLAP:
            if ((self.file_format == exclude[0] and other.file_format == exclude[1]) or (self.file_format == exclude[1] and other.file_format == exclude[0])):
                return True
        return False

    def compare(self, other):
        if self.tag == None and other.tag == None:
            return False
        
        tagEqual = self.compareTag(other) != None

        if tagEqual == False:
            return False

        if self.tag_category != other.tag_category:
            selfTag = tag_to_str(self.tag)
            otherTag = tag_to_str(other.tag)
            raise ApplangaConfigFileNotValidException(f'Inconsistent tag_category for tag(s): "{self.tag_category}" for {selfTag} VS "{other.tag_category}" for {otherTag}.')
        
        if self.ignoreFormatOverlap(other):
            return False
        
        if self.language == None:
            if other.language == None:
                if set(self.exclude_languages).intersection(other.exclude_languages):
                    return True
            else:
                if other.language not in self.exclude_languages:
                    return True
        else:
            if other.language == None:
                if self.language not in other.exclude_languages:
                    return True
            else:
                if self.language == other.language:
                    return True
        return False
    

    def __str__(self):
        return '''{language}:{tag}:{path}:{exc}:{format}'''.format(tag=self.tag, language=self.language, path=self.path, exc=self.exclude_languages, format=self.file_format)

def tag_to_str(tag):
    return json.dumps(tag)

def testTagConflict(config_data):
    push_map = {}
    if 'push' in config_data['app']:
        # to spare us some backend requests sort all entries that have the <language> var to the end so we can compare with statically set langs overlaps
        config_data['app']['push']['source'].sort(key=cmp_to_key(lambda a, b: +1 if 'path' in a and '<language>' in a['path'] else -1 if 'path' in b and '<language>' in b['path'] else 0))
        
        blocks = []
        for push_conf in config_data['app']['push']['source']:
            blocks.append(FileBlock(push_conf))
        
        for i, blockA in enumerate(blocks):
            for j, blockB in enumerate(blocks):
                if i == j or j < i: continue
                if blockA.compare(blockB):
                    lang = blockA.language
                    if lang == None:
                        lang = "<language>"
                    
                    raise ApplangaConfigFileNotValidException('''The tag "{tag}" is used across multiple files for the language "{language}" in your push block. Please ensure tags are unique per file'''.format(tag=blockA.compareTag(blockB), language=lang))

    if 'pull' in config_data['app']:
        # to spare us some backend requests sort all entries that have the <language> var to the end so we can compare with statically set langs overlaps
        config_data['app']['pull']['target'].sort(key=cmp_to_key(lambda a, b: +1 if 'path' in a and '<language>' in a['path'] else
                                                                                -1 if 'path' in b and '<language>' in b['path'] else 0))
        
        blocks = []
        for push_conf in config_data['app']['pull']['target']:
            blocks.append(FileBlock(push_conf))

        for i, blockA in enumerate(blocks):
            for j, blockB in enumerate(blocks):
                if i == j or j < i: continue
                if blockA.compare(blockB):
                    lang = blockA.language
                    if lang == None:
                        lang = "<language>"
                    raise ApplangaConfigFileNotValidException('''The tag "{tag}" is used across multiple files for the language "{language}" in your pull block. Please ensure tags are unique per file'''.format(tag=blockA.compareTag(blockB), language=lang))





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