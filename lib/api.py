import click
import requests
import json
import os
import errno
import re
import time
from lib import constants
from lib import config_file
from lib import files

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

class ApplangaRequestException(Exception):
    pass



def downloadFile(file_data, debug=False):
    """Downloads file from Applanga.

    Args:
        file_data: Data about the files to download.
        debug: Display debug output.

    Returns:
        Path of file which got downloaded

    """

    # Make sure it contains all the data that is needed
    if 'language' not in file_data:
        raise ApplangaRequestException('Request is incomplete. The language is missing.')
    if 'file_format' not in file_data:
        raise ApplangaRequestException('Request is incomplete. The file_format is missing.')
    if 'path' not in file_data:
        raise ApplangaRequestException('Request is incomplete. The path is missing.')


    request_options = {}
    request_options['exportOnlyWithTranslation'] = True

    if 'export_empty' in file_data:
        if file_data['export_empty'] == True:
            request_options['exportOnlyWithTranslation'] = False

    if 'convert_placeholder' in file_data:
        if file_data['convert_placeholder'] == True:
            request_options['convertPlaceholder'] = True

    if 'ignore_duplicates' in file_data:
        request_options['ignoreDuplicates'] = file_data['ignore_duplicates'] is True
        
    if file_data['file_format'] in ['nested_json', 'react_nested_json', 'ruby_on_rails_yaml', 'symfony_yaml', 'symfony2_yaml', 'ember_i18n_json_module', 'node_2_json', 'go_i18n_json'] and 'disable_plurals' in file_data:
            request_options['disablePlurals'] = file_data['disable_plurals'] is True

    if 'includeMetadata' in file_data:
        request_options['includeMetadata'] = file_data['includeMetadata']
    
    if 'includeInvisibleId' in file_data:
        request_options['includeInvisibleId'] = file_data['includeInvisibleId']

    if 'xliffStatus' in file_data:
        request_options['xliffStatus'] = file_data['xliffStatus']

    if 'includeContextUrl' in file_data:
        request_options['includeContextUrl'] = file_data['includeContextUrl']

    # check conditions for key_prefix
    if 'key_prefix' in file_data:
        if len(file_data['key_prefix']) > 50:
            raise ApplangaRequestException('The key prefix cannot be longer than 50 characters: %s\nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.' % (file_data['key_prefix']))

        pattern = re.compile('^[a-zA-Z0-9 _-]*$')
        matchPatter = pattern.match(file_data['key_prefix'])
        if not matchPatter:
            raise ApplangaRequestException('The key prefix can contain only letters, numbers, space, undescore and dash: %s\nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.' % (file_data['key_prefix']))

    if 'sort_by_key' in file_data:
        if file_data['sort_by_key'] == True:
            request_options['sortByKey'] = True

    if 'remove_cr_char' in file_data:
        if file_data['remove_cr_char'] == True:
            request_options['removeCrChar'] = True

    try:
        # Request the file from server
        request_data = {
            'file-format': file_data['file_format'],
            'language': file_data['language'],
            'options': json.dumps(request_options)
        }
        if 'tag' in file_data:
            request_data['tag'] = file_data['tag']
        
        if 'key_prefix' in file_data:
            request_data['removeKeyPrefix'] = file_data['key_prefix']

        request_data['version'] = file_data['projectVersion']

        response = makeRequest(data=request_data, api_path='/files', debug=debug)

    except ApplangaRequestException as e:
        raise ApplangaRequestException(str(e))

    language = file_data['language']

    language_ = language.replace('-', '_')
    if 'android_xml' == file_data['file_format'] and len(language) == 5:
        language = language.replace('-', '-r')


    if 'arb' == file_data['file_format'] and len(language) >= 5:
        language = language_

    try:
        config_file_data = config_file.readRaw()
        languageMapping = config_file_data['languageMap']
        if languageMapping[language]:
            language = languageMapping[language]
    except Exception as e:
        pass
    

    #if we detect a language folder with an _ locale but non with - we store the files int the _ folder
    file_path = file_data['path'].replace('<language>', language)
    file_path_ = file_data['path'].replace('<language>', language_)
    if not os.path.exists(os.path.dirname(file_path)) and os.path.exists(os.path.dirname(file_path_)):
        file_path = file_path_
        
    try:
        # Makes sure that the directory we want to write into exists
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        open(file_path, 'wb').write(response.content)
        return file_path
    except FileNotFoundError as e:
        raise ApplangaRequestException('Could not write file "%s": %s' % (file_path, str(e)))



def uploadFiles(upload_files, force=False, draft=False, debug=False):
    """Uploads multiple files to Applanga.

    Args:
        file_data: Data about the files to upload.
        debug: Display debug output.

    Returns:
        API response

    """

    placeholder_files = {}

    return_data = []

    files_to_upload = [];

    for source in upload_files:
        # Check if we have the data we need for sure
        if 'path' not in source:
            return_data.append(
                {
                    'path': 'unknown',
                    'error': 'No path defined'
                }
            )
            continue
        if 'file_format' not in source:
            return_data.append(
                {
                    'path': source['path'],
                    'error': 'No file-format defined'
                }
            )
            continue
        if 'path' in source and source['path'].find('<language>') == -1 and 'language' not in source:
            return_data.append(
                {
                    'path': source['path'],
                    'error': 'You either need to use the <language> wildcard inside the path string or set it explicitly per file via the "language" property. \nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.'
                }
            )
            continue

        # check conditions for key_prefix
        if 'path' in source and 'key_prefix' in source:
            if len(source['key_prefix']) > 50:
                return_data.append(
                    {
                        'path': source['key_prefix'],
                        'error': 'The key prefix cannot be longer than 50 characters. \nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.'
                    }
                )
                continue
            pattern = re.compile('^[a-zA-Z0-9 _-]*$')
            matchPatter = pattern.match(source['key_prefix'])
            if not matchPatter:
                return_data.append(
                    {
                        'path': source['key_prefix'],
                        'error': 'The key prefix can contain only letters, numbers, space, undescore and dash. \nFor more informations and examples on how todo that please refer to the Applanga CLI Integration Documentation.'
                    }
                )
                continue

        language_files = files.getFiles(source)

        files_to_upload.append(language_files['found'])

        if language_files['uses_placeholder'] == True:
            placeholder_files.update()

    # Upload all the files
    for files_data in files_to_upload:

        for file_path in files_data:
            file_data = files_data[file_path]

            # Make sure it contains all the data that is needed
            if 'file_format' not in file_data:
                return_data.append(
                    {
                        'language': file_data['language'],
                        'path': file_path,
                        'error': 'Request is incomplete. The file_format is missing.'
                    }
                )

            try:
                send_data = {
                    'file_format':  file_data['file_format'],
                    'language': file_data['language'],
                    'path': file_path
                }

                if 'tag' in file_data:
                    send_data['tag'] = file_data['tag']

                if 'keepTagIds' in file_data:
                    send_data['keepTagIds'] = file_data['keepTagIds']

                if 'key_prefix' in file_data:
                    send_data['key_prefix'] = file_data['key_prefix']

                if  'disable_plurals' in file_data:
                    send_data['disable_plurals'] = file_data['disable_plurals']

                if 'xliffStatus' in file_data:
                    send_data['xliffStatus'] = file_data['xliffStatus']

                if file_data['file_format'] in ['xliff'] and 'skipLockedTranslations' in file_data:
                    send_data['skipLockedTranslations'] = file_data['skipLockedTranslations']

                if file_data['file_format'] in ['xliff'] and 'skipEmptyTranslations' in file_data:
                    send_data['skipEmptyTranslations'] = file_data['skipEmptyTranslations']

                if file_data['file_format'] in ['xliff'] and 'createUnknownCustomStates' in file_data:
                    send_data['createUnknownCustomStates'] = file_data['createUnknownCustomStates']

                if 'remove_cr_char' in file_data:
                    send_data['removeCrChar'] = file_data['remove_cr_char']

                if 'onlyIfTextEmpty' in file_data and file_data['file_format'] in ['xliff']:
                    send_data['onlyIfTextEmpty'] = file_data['onlyIfTextEmpty']

                if file_data['file_format'] in ['xliff'] and'onlyAsDraft' in file_data:
                    send_data['onlyAsDraft'] = file_data['onlyAsDraft']

                if file_data['file_format'] in ['xliff'] and 'importSourceLanguage' in file_data:
                    send_data['importSourceLanguage'] = file_data['importSourceLanguage']

                response = uploadFile(send_data, force=force, draft=draft, debug=debug)
                return_data.append(
                    {
                        'language': file_data['language'],
                        'path': file_path,
                        'response': response
                    }
                )
            except ApplangaRequestException as e:
                return_data.append(
                    {
                        'language': file_data['language'],
                        'path': file_path,
                        'error': str(e)
                    }
                )

    return return_data



def uploadFile(file_data, force=False, draft=False, debug=False):
    """Uploads a file to Applanga.

    Args:
        file_data: Data about the file to upload.
        debug: Display debug output.

    Returns:
        API response

    """

    try:
        # Request the file from server
        request_options = {
            'onlyIfTextEmpty': not force,
            'onlyAsDraft': draft,
        }

        if file_data['file_format'] in ['nested_json', 'react_nested_json'] and 'disable_plurals' in file_data:
            request_options['disablePlurals'] = file_data['disable_plurals'] is True

        if file_data['file_format'] in ['xliff'] and 'importSourceLanguage' in file_data:
            request_options['importSourceLanguage'] = file_data['importSourceLanguage']

        if file_data['file_format'] in ['xliff'] and 'xliffStatus' in file_data:
            request_options['xliffStatus'] = file_data['xliffStatus']

        if file_data['file_format'] in ['xliff'] and 'createUnknownCustomStates' in file_data:
            request_options['createUnknownCustomStates'] = file_data['createUnknownCustomStates']

        if 'skipLockedTranslations' in file_data and file_data['file_format'] in ['xliff']:
            request_options['skipLockedTranslations'] = file_data['skipLockedTranslations']

        if file_data['file_format'] in ['xliff'] and 'skipEmptyTranslations' in file_data:
            request_options['skipEmptyTranslations'] = file_data['skipEmptyTranslations']

        if file_data['file_format'] in ['xliff'] and 'onlyIfTextEmpty' in file_data:
            request_options['onlyIfTextEmpty'] = file_data['onlyIfTextEmpty']
        elif file_data['file_format'] in ['xliff']:
            request_options['onlyIfTextEmpty'] = True

        if file_data['file_format'] in ['xliff'] and'onlyAsDraft' in file_data:
            request_options['onlyAsDraft'] = file_data['onlyAsDraft']

        if 'removeCrChar' in file_data:
            request_options['removeCrChar'] = file_data['removeCrChar']

        request_data = {
            'file-format': file_data['file_format'],
            'language': file_data['language'],
            'options': json.dumps(request_options)
        }

        if 'tag' in file_data:
            request_data['tag'] = file_data['tag']

        if 'keepTagIds' in file_data:
            request_data['keepTagIds'] = file_data['keepTagIds']

        if 'key_prefix' in file_data:
            request_data['addKeyPrefix'] = file_data['key_prefix']

        return makeRequest(data=request_data, api_path='/files', upload_file=file_data['path'], method='POST', debug=debug)
    except ApplangaRequestException as e:
        raise ApplangaRequestException(str(e))



def getAllAppLanguages(projectVersion, debug):
    """Gets all the languages the app has defined

    Args:
        debug: Display debug output.

    Returns:
        Array of languages
    """

    data = {
        'includeDraft': 'false',
        'includeValue' : 'false',
        'includeSrc': 'false',
        'includeDescription' : 'false',
        'includeStatus' : 'false',
        'keepEmptyDataEntries' : 'true',
        'version': projectVersion
    }

    response = makeRequest(data=data, debug=debug)
    response_data = response.json()

    if 'data' not in response_data:
        raise ApplangaRequestException('Response is incomplete. Data property is missing.')

    return response_data['data'].keys();



def getProjectVersion(debug):
    """Gets the latest project version

    Args:
        debug: Display debug output.

    Returns:
        Version number
    """
    request_data = {
        'timestamp': time.time()
    }

    response = makeRequest(data=request_data, api_path='/projectVersion', debug=debug)
    response_data = response.json()

    if 'appVersion' not in response_data:
        return 0;

    return response_data['appVersion'];



def makeRequest(data={}, api_path=None, access_token=None, upload_file=None, method='GET', debug=False, base_path=constants.API_BASE_PATH):
    """Makes a request to Applanga API.

    Args:
        data: Data to send to API.
        api_path: Path to append to API URL.
        access_token: The access token to use.
        upload_file: File to upload with request.
        method: Request method to use.
        debug: Display debug output.
        base_url: Api base path if specified will overwrite default '/v1/api'

    Returns:
        API response

    """

    config_file_data = None
    branch_id = None
    if access_token is None:
        # No access_token given so try to get from config file and stop when
        # nothing gets returned
        try:
            config_file_data = config_file.readRaw()
        except config_file.ApplangaConfigFileNotValidException as e:
            raise ApplangaRequestException(str(e))

        access_token = config_file_data['app']['access_token']
        if 'branch_id' in config_file_data['app']:
            branch_id = config_file_data['app']['branch_id']

    if not access_token:
        if not config_file_data:
            raise ApplangaRequestException('Access token is missing')

    # App id is part of access token. Extract it to additionally also send
    # separate as parameter as needed by API.
    app_id = access_token.split('!')[0]

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'CLI-Version': constants.VERSION_NUMBER,
        'X-Integration': constants.X_INTEGRATION_HEADER_VALUE
    }

    url = constants.APPLANGA_HOST

    env_api_base_url = os.environ.get('APPLANGA_API_HOST')

    if env_api_base_url:
        url = env_api_base_url

    url = url + base_path
    

    if api_path is not None:
        url += api_path

    data['app'] = app_id
    if branch_id is not None:
        data['branch'] = branch_id


    if debug:
        click.secho('\nStart request:', fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  URL: %s'  % (url), fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  Method: %s'  % (method), fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  Headers: %s'  % (headers), fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  Data: %s'  % (data), fg=constants.DEBUG_TEXT_COLOR)

    if method == 'GET':
        try:
            response = requests.get(url, params=data, headers=headers)
        except requests.exceptions.ConnectionError as e:
            raise ApplangaRequestException('Problem connecting to server. Please check your internet connection.')
    else:
        if upload_file:
            try:
                with open(upload_file, 'rb') as upload_file_content:
                    try:
                        response = requests.post(url, params=data, headers=headers, files={upload_file: upload_file_content})
                    except requests.exceptions.ConnectionError as e:
                        raise ApplangaRequestException('Problem connecting to server. Please check your internet connection.')

            except IOError as e:
                click.echo(e)
                raise ApplangaRequestException('Problem with accessing file to upload. The file does probably not exist or there are problems with the access rights.')

        else:
            response = requests.post(url, params=data, headers=headers)

    if debug:
        click.secho('\nRequest response: %s' % response.text, fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  Status code: %s'  % (response.status_code), fg=constants.DEBUG_TEXT_COLOR)


    if response.status_code != 200:
        # Request was not successful so raise exception
        exception_text = response.text

        try:
            response_data = response.json()
            if 'message' in response_data:
                # There is a message so return it
                exception_text = response_data['message']
        except ValueError as e:
            exception_text = response.text

        raise ApplangaRequestException('API response: ' + exception_text)

    # Request was successful so return
    return response
