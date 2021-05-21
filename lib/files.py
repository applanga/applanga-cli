import click
import glob2
import re
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
        language_regex_path = re.escape(path).replace('\*', '.*').replace(re.escape('<language>'), '([a-zA-Z]{2}([\-\_][a-zA-Z]{2,4})?)')
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
            if 'file_format' in source:
                return_files[file]['file_format'] = source['file_format']

            if 'disable_plurals' in source:
                return_files[file]['disable_plurals'] = source['disable_plurals']


    return {
                'skipped': skipped_files,
                'found': return_files,
                'uses_placeholder': uses_placeholder
            }
