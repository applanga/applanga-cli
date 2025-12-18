VERSION_NUMBER = '1.0.115'
APPLANGA_HOST = 'https://api.applanga.com'
API_BASE_PATH = '/v1/api'
CONFIG_FILE_NAME = '.applanga.json'
DEBUG_TEXT_COLOR = 'blue'
ENVIRONMENT_VARIABLE = 'APPLANGA_CONFIG'
X_INTEGRATION_HEADER_VALUE = '1'
EXCLUDE_FORMAT_OVERLAP = [['ios_strings', 'ios_stringsdict']]
FILE_FORMATS = {
    'android_xml': {
        'name': 'Android XML',
        'extension': 'xml',
        'default_baselanguage_path': './res/values/strings.xml',
        'default_file_path': './res/values-<language>/strings.xml',
        'default_tag_name': 'app:strings.xml'
    },
    'angular_translate_json': {
        'name': 'Angular Translate JSON',
        'extension': 'json',
        'default_file_path': './i18n/<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'chrome_i18n_json': {
        'name': 'Chrome i18n JSON',
        'extension': 'json',
        'default_file_path': './_locales/<language>/messages.json',
        'default_tag_name': 'app:messages.json'
    },
    'ember_i18n_json_module': {
        'name': 'Ember i18n JSON Module',
        'extension': 'js',
        'default_file_path': './app/locales/<language>/translations.js',
        'default_tag_name': 'app:translations.js'
    },
    'mozilla_i18n_json': {
        'name': 'Mozilla i18n JSON',
        'extension': 'json',
        'default_file_path': './_locales/<language>/messages.json',
        'default_tag_name': 'app:messages.json'
    },
    'nested_json': {
        'name': 'Nested JSON',
        'extension': 'json',
        'default_file_path': './<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'ini': {
        'name': 'Ini File',
        'extension': 'ini',
        'default_file_path': './<language>.ini',
        'default_tag_name': 'app:language.ini'
    },
    'ios_strings': {
        'name': 'iOS strings',
        'extension': 'strings',
        'default_baselanguage_path': './Base.lproj/Localizable.strings',
        'default_file_path': './<language>.lproj/Localizable.strings',
        'default_tag_name': 'app:Localizable.strings'
    },
    'ios_stringsdict': {
        'name': 'iOS stringsdict',
        'extension': 'stringsdict',
        'default_baselanguage_path': './Base.lproj/Localizable.stringsdict',
        'default_file_path': './<language>.lproj/Localizable.stringsdict',
        'default_tag_name': 'app:Localizable.strings'
    },
    'java_properties': {
        'name': 'JAVA properties',
        'extension': 'properties',
        'default_file_path': './ApplicationMessages_<language>.properties',
        'default_tag_name': 'app:ApplicationMessages.properties'
    },
    'gettext_po': {
        'name': 'Gettext PO File',
        'extension': 'po',
        'default_file_path': './<language>.po',
        'default_tag_name': 'app:language.po'
    },
    'gettext_pot': {
        'name': 'Gettext POT File',
        'extension': 'pot',
        'default_file_path': './<language>.pot',
        'default_tag_name': 'app:language.po'
    },
    'go_i18n_json': {
        'name': 'go-i18n v1 JSON',
        'extension': 'json',
        'default_file_path': './<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'microsoft_resw': {
        'name': 'Microsoft Resource File',
        'extension': 'resw',
        'default_file_path': './<language>.resw',
        'default_tag_name': 'app:language.resw'
    },
    'microsoft_resx': {
        'name': 'Microsoft Resource File',
        'extension': 'resx',
        'default_file_path': './<language>.resx',
        'default_tag_name': 'app:language.resx'
    },
    'mozilla_properties': {
        'name': 'Mozilla properties',
        'extension': 'properties',
        'default_file_path': './ApplicationMessages_<language>.properties',
        'default_tag_name': 'app:ApplicationMessages.properties'
    },
    'node_2_json': {
        'name': 'i18n-node-2',
        'extension': 'json',
        'default_file_path': './locales/<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'i18next_json': {
        'name': 'i18next',
        'extension': 'json',
        'default_file_path': './locales/<language>/translations.json',
        'default_tag_name': 'app:translations.json'
    },
    'react_simple_json': {
        'name': 'React Simple JSON',
        'extension': 'json',
        'default_file_path': './<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'react_nested_json': {
        'name': 'React Nested JSON',
        'extension': 'json',
        'default_file_path': './<language>.json',
        'default_tag_name': 'app:language.json'
    },
    'ruby_on_rails_yaml': {
        'name': 'Ruby on Rails YAML',
        'extension': 'yaml',
        'default_file_path': './<language>.yaml',
        'default_tag_name': 'app:language.yaml'
    },
    'symfony_yaml': {
        'name': 'Symfony YAML',
        'extension': 'yaml',
        'default_file_path': './<language>.yaml',
        'default_tag_name': 'app:language.yaml'
    },
    'symfony2_yaml': {
        'name': 'Symfony 2 YAML',
        'extension': 'yaml',
        'default_file_path': './<language>.yaml',
        'default_tag_name': 'app:language.yaml'
    },
    'laravel_php': {
        'name': 'PHP Laravel',
        'extension': 'php',
        'default_file_path': './<language>.php',
        'default_tag_name': 'app:language.php'
    },
    'arb': {
        'name': 'Flutter ARB',
        'extension': 'arb',
        'default_file_path': './<language>.arb',
        'default_tag_name': 'app:language.arb'
    },
    'qt_ts': {
        'name': 'Qt Linguist',
        'extension': 'ts',
        'default_file_path': './<language>.ts',
        'default_tag_name': 'app:language.ts'
    },
    'toml': {
        'name': 'TOML',
        'extension': 'toml',
        'default_file_path': './<language>.toml',
        'default_tag_name': 'app:language.toml'
    },
    'xliff': {
        'name': 'Xliff',
        'extension': 'xliff',
        'default_file_path': './<language>.xliff',
        'default_tag_name': 'app:language.xliff'
    },
    'csv': {
        'name': 'CSV File',
        'extension': 'csv',
        'default_file_path': './<language>.csv',
        'default_tag_name': 'app:language.csv'
    },
    'tsv': {
        'name': 'TSV File',
        'extension': 'tsv',
        'default_file_path': './<language>.tsv',
        'default_tag_name': 'app:language.tsv'
    },
    'xls': {
        'name': 'Excel',
        'extension': 'xls',
        'default_file_path': './<language>.xls',
        'default_tag_name': 'app:language.xls'
    }
}

TAG_NAME_CHAR_LIMIT = 400