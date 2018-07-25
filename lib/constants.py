VERSION_NUMBER = '1.0.0'
# API_BASE_URL = 'https://api.applanga.com/v1/api'
API_BASE_URL = 'http://localhost:3000/v1/api'
CONFIG_FILE_NAME = '.applanga.json'
DEBUG_TEXT_COLOR = 'blue'
ENVIRONMENT_VARIABLE = 'APPLANGA_CONFIG'
FILE_FORMATS = {
    'android_xml': {
        'name': 'Android XML',
        'extension': 'xml',
        'default_file_path': './res/values-<language>/strings.xml'
    },
    'angular_translate_json': {
        'name': 'Angular Translate JSON',
        'extension': 'json',
        'default_file_path': './locale-<language>.json'
    },
    'chrome_i18n_json': {
        'name': 'Chrome i18n JSON',
        'extension': 'json',
        'default_file_path': './_locales/<language>/messages.json'
    },
    'mozilla_i18n_json': {
        'name': 'Mozilla i18n JSON',
        'extension': 'json',
        'default_file_path': './_locales/<language>/messages.json'
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
    'java_properties': {
        'name': 'JAVA properties',
        'extension': 'properties',
        'default_file_path': './ApplicationMessages_<language>.properties'
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
    'go_i18n_translate_json': {
        'name': 'go-i18n JSON',
        'extension': 'json',
        'default_file_path': './<language>.json'
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
    },
    'mozilla_properties': {
        'name': 'Mozilla properties',
        'extension': 'properties',
        'default_file_path': './ApplicationMessages_<language>.properties'
    },
    'node_2_json': {
        'name': 'i18n-node-2',
        'extension': 'json',
        'default_file_path': './locales/<language>.json'
    },
    'i18next_json': {
        'name': 'i18next',
        'extension': 'json',
        'default_file_path': './locales/<language>/translations.json'
    },
}
