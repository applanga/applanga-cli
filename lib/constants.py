API_BASE_URL = 'https://api.applanga.com/v1/api'
CONFIG_FILE_NAME = '.applanga.json'
DEBUG_TEXT_COLOR = 'blue'
ENVIRONMENT_VARIABLE = 'APPLANGA_CONFIG'
FILE_FORMATS = {
    'android_xml': {
        'name': 'Android XML',
        'default_file_path': './res/values-<language>/strings.xml'
    },
    'ios_strings': {
        'name': 'iOS strings',
        'default_file_path': './<language>.lproj/Localizable.strings'
    },
    'ios_stringsdict': {
        'name': 'iOS stringsdict',
        'default_file_path': './<language>.lproj/Localizable.stringsdict'
    }
}