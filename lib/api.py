import click
import requests
import json
import os
from lib import constants
from lib import config_file
from lib import files



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


    try:
        # Request the file from server
        request_data = {
            'file-format': file_data['file_format'],
            'language': file_data['language'],
            'options': json.dumps(request_options)
        }
        if 'tag' in file_data:
            request_data['tag'] = file_data['tag']

        response = makeRequest(data=request_data, api_path='/files', debug=debug)

    except ApplangaRequestException as e:
        raise ApplangaRequestException(str(e))

    file_path = file_data['path'].replace('<language>', file_data['language'])
    try:
        # Makes sure that the directory we want to write into exists
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as e:
                if e.errno != os.errno.EEXIST:
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
        request_data = {
            'file-format': file_data['file_format'],
            'language': file_data['language'],
            'options': json.dumps({
                'onlyIfTextEmpty': not force,
                'onlyAsDraft': draft
            })
        }
        if 'tag' in file_data:
            request_data['tag'] = file_data['tag']

        return makeRequest(data=request_data, api_path='/files', upload_file=file_data['path'], method='POST', debug=debug)
    except ApplangaRequestException as e:
        raise ApplangaRequestException(str(e))



def getAllAppLanguages(debug):
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
        'keepEmptyDataEntries' : 'true'
    }

    response = makeRequest(data=data, debug=debug)
    response_data = response.json()

    if 'data' not in response_data:
        raise ApplangaRequestException('Response is incomplete. Data property is missing.')

    return response_data['data'].keys();



def makeRequest(data={}, api_path=None, access_token=None, upload_file=None, method='GET', debug=False):
    """Makes a request to Applanga API.

    Args:
        data: Data to send to API.
        api_path: Path to append to API URL.
        access_token: The access token to use.
        upload_file: File to upload with request.
        method: Request method to use.
        debug: Display debug output.

    Returns:
        API response

    """

    config_file_data = None
    if access_token is None:
        # No access_token given so try to get from config file and stop when
        # nothing gets returned
        try:
            config_file_data = config_file.readRaw()
        except config_file.ApplangaConfigFileNotValidException as e:
            raise ApplangaRequestException(str(e))

        access_token = config_file_data['app']['access_token']

    if not access_token:
        if not config_file_data:
            raise ApplangaRequestException('Access token is missing')

    # App id is part of access token. Extract it to additionally also send
    # separate as parameter as needed by API.
    app_id = access_token.split('!')[0]

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'CLI-Version': constants.VERSION_NUMBER
    }
    url = constants.API_BASE_URL

    if api_path is not None:
        url += api_path

    data['app'] = app_id

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
        click.secho('\nRequest response:', fg=constants.DEBUG_TEXT_COLOR)
        click.secho('  Status code: %s'  % (response.status_code), fg=constants.DEBUG_TEXT_COLOR)


    if response.status_code is not 200:
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
