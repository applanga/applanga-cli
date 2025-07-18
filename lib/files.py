import click
import glob2
import re
import copy
from lib import config_file


class ApplangaTranslationsException(Exception):
    pass



def convertToWindowsPath(path):
    """Converts a Unix file path to a Windows one.

    Args:
        path: The path in Unix format.

    Returns:
        The converted path in Windows format.

    """
    return path.replace('/', '\\')



def convertLanguageName(language_name):
    """Converts language names into format Applanga API expects.

    Args:
        language_name: The language name to convert.

    Returns:
        The converted language or None if conversion was not possible.

    """
    if '-' in language_name or '_' in language_name:
        split_name = language_name.split('-')
        if len(split_name) != 2:
            split_name = language_name.split('_')
            if len(split_name) != 2:
                # It has to have exactly two parts else it is not valid
                return None

        second_part = split_name[1].lower();

        if len(second_part) == 2:
            # Normally the most have only two letters so return
            return split_name[0].lower() + '-' + split_name[1].upper()
        elif len(second_part) == 3 and second_part[0] == 'r':
            # android prefixes the region with an lowercase r
            return split_name[0].lower() + '-' + second_part[1:].upper()
        elif len(second_part) == 4:
            # Two special cases of 4 letter ones that are supported
            if second_part == 'hant':
                return split_name[0].lower() + '-Hant'
            elif second_part == 'hans':
                return split_name[0].lower() + '-Hans'

    else:
        return language_name.lower()

    return None


def getFiles(source):
    """Looks and retruns files which match path in given source block.

    Args:
        source: The source block dictionary with path property.

    Returns:
        The found files with language and skipped ones for which no language could be found.

    """

    return_files = {}
    skipped_files = []

    path = source['path']

    source_language = None
    language_regex_path = None
    search_path = path
    uses_placeholder = False

    if 'language' in source:
        # Language is given as parameter
        source_language = source['language']
    else:
        # Language is in path
        search_path = path.replace('<language>', '*')
        language_regex_path = re.escape(path).replace(r'\*', '.*').replace(re.escape('<language>'), r'([a-zA-Z]{2}([\-\_][a-zA-Z]{2,4})?)')
        uses_placeholder = True

    files = glob2.glob(search_path)

    # Go through all matched files of the current source block and add them
    # according to their language
    for file in files:
        file_language = None

        if language_regex_path:
            # If a regex is defined try to get language from path
            file_match = re.search(language_regex_path, file)
            if file_match and len(file_match.groups()):
                file_language = file_match.group(1)

        if not file_language:
            # If no language got found in path use the one from source
            # block if defined
            file_language = source_language

        if file_language:
            try:
                config_file_data = config_file.readRaw()
                reversedDir = dict(map(reversed, config_file_data['languageMap'].items()))
                file_language = reversedDir[file_language]
            except (config_file.ApplangaConfigFileNotValidException, KeyError) as e:
                pass
            
                    
            # Make sure the language name is in the correct format
            file_language = convertLanguageName(file_language)

            if file_language == None:
                skipped_files.append(file)
                continue

            # Remove all the languages on the exclude list
            if 'exclude_languages' in source:
                if file_language in source['exclude_languages']:
                    continue

            return_files[file] = {'language': file_language}

            # Add other properties which got defined for file
            if 'tag' in source:
                return_files[file]['tag'] = source['tag']
            if 'keepTagIds' in source:
                return_files[file]['keepTagIds'] = source['keepTagIds']
            if 'file_format' in source:
                return_files[file]['file_format'] = source['file_format']
            if 'key_prefix' in source:
                return_files[file]['key_prefix'] = source['key_prefix']
            if 'remove_cr_char' in source:
                return_files[file]['remove_cr_char'] = source['remove_cr_char']

            if 'disable_plurals' in source:
                return_files[file]['disable_plurals'] = source['disable_plurals']

            #'importStatus' overwrites 'xliffStatus' if both are present
            if 'xliffStatus' in source:
                return_files[file]['importStatus'] = source['xliffStatus']
            if 'importStatus' in source:
                return_files[file]['importStatus'] = source['importStatus']

            if 'createUnknownCustomStates' in source:
                return_files[file]['createUnknownCustomStates'] = source['createUnknownCustomStates']
            if 'importSourceLanguage' in source:
                return_files[file]['importSourceLanguage'] = source['importSourceLanguage']
            if 'skipLockedTranslations' in source: 
                return_files[file]['skipLockedTranslations'] = source['skipLockedTranslations']
            if 'skipEmptyTranslations' in source: 
                return_files[file]['skipEmptyTranslations'] = source['skipEmptyTranslations']
            if 'onlyIfTextEmpty' in source: 
                return_files[file]['onlyIfTextEmpty'] = source['onlyIfTextEmpty']
            if 'onlyAsDraft' in source: 
                return_files[file]['onlyAsDraft'] = source['onlyAsDraft']
            if 'importIntoGroup' in source: 
                return_files[file]['importIntoGroup'] = source['importIntoGroup']

            if 'columnDescription' in source:
                returnedColumnDescription = copy.deepcopy(source['columnDescription'])
                if '<language>' in source['columnDescription']:
                    #only replace '<language>' if the same languiages does not yet exist in the 'columnDescription'
                    if file_language not in source['columnDescription'] :
                        returnedColumnDescription[file_language] = source['columnDescription']['<language>']
                    del returnedColumnDescription['<language>']
                return_files[file]['columnDescription'] = returnedColumnDescription
            if 'sheetName' in source:
                return_files[file]['sheetName'] = source['sheetName']
            if 'excludeHeaderRow' in source:
                return_files[file]['includeFirstRow'] = source['excludeHeaderRow']
            if 'skipNonStringValues' in source:
                return_files[file]['skipNonStringValues'] = source['skipNonStringValues']
            if 'autoGenerateMissingKeys' in source:
                return_files[file]['autoGenerateMissingKeys'] = source['autoGenerateMissingKeys']

    return {
                'skipped': skipped_files,
                'found': return_files,
                'uses_placeholder': uses_placeholder
            }
