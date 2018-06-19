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
    if '-' in language_name:
        split_name = language_name.split('-')
        if len(split_name) != 2:
            # It has to have exactly two parts else it is not valid
            return None
        return split_name[0].lower() + '-' + split_name[1].upper()
    else:
        return language_name.lower()



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

    if 'language' in source:
        # Language is given as parameter
        source_language = source['language']
    else:
        # Language is in path
        search_path = path.replace('<language>', '*')
        language_regex_path = re.escape(path).replace('\*', '.*').replace('\<language\>', '([a-zA-Z]{2}(\-[a-zA-Z]{2})?)')

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

            if file_language not in return_files:
                return_files[file_language] = []
            return_files[file_language].append(file)
        else:
            skipped_files.append(file)

    return {
                'skipped': skipped_files,
                'found': return_files
            }
