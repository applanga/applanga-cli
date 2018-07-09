VERSION_NUMBER = '1.0.0'
API_BASE_URL = 'https://api.applanga.com/v1/api'
CONFIG_FILE_NAME = '.applanga.json'
DEBUG_TEXT_COLOR = 'blue'
ENVIRONMENT_VARIABLE = 'APPLANGA_CONFIG'
FILE_FORMATS = {
    'android_xml': {
        'name': 'Android XML',
        'extension': 'xml',
        'default_file_path': './res/values-<language>/strings.xml'
    },
    'ios_strings': {
        'name': 'iOS strings',
        'extension': 'strings',
        'default_file_path': './<language>.lproj/Localizable.strings'
    },
    'ios_stringsdict': {
        'name': 'iOS stringsdict',
        'extension': 'stringsdict',
        'default_file_path': './<language>.lproj/Localizable.stringsdict'
    },
    'gettext_po': {
        'name': 'Gettext PO File',
        'extension': 'po',
        'default_file_path': './<language>.po'
    },
    'gettext_pot': {
        'name': 'Gettext POT File',
        'extension': 'pot',
        'default_file_path': './<language>.pot'
    },
    'microsoft_resw': {
        'name': 'Microsoft Resource File',
        'extension': 'resw',
        'default_file_path': './<language>.resw'
    },
    'microsoft_resx': {
        'name': 'Microsoft Resource File',
        'extension': 'resx',
        'default_file_path': './<language>.resx'
    }
}
