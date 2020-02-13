# Applanga Localization Command Line Interface (CLI)

***
*Version:* 1.0.44

*Website:* <https://www.applanga.com>

*Changelog:* <https://www.applanga.com/changelog/cli>
***

## Table of Contents

  1. [Installation](#installation)
  2. [Initialization](#initialize-project)
  3. [Usage](#push-pull-translation-files)
  4. [Configuration](#configuration)
  5. [Configuration Examples](#configuration-examples)
	- [Android Examples](#android-configuration-examples)
	- [iOS Examples](#ios-configuration-examples)

## Installation

##### Manual

1. [Download and extract](https://github.com/applanga/applanga-cli/releases/latest) the latest client binary for your platform.

2. Store the binary at a location where it can be found and executed by the system or adjust your [PATH](https://en.wikipedia.org/wiki/PATH_(variable)) accordingly

3. You should now be able to execute it on the command-line like:

```sh
	applanga --help
```
or

```sh
	applanga.exe --help
```


##### Homebrew

On OSX we provide a homebrew tap to make the installation easier and up to date:

```sh
	brew tap applanga/cli
	brew install applanga
```

To update to the latest version call:

```sh
	brew upgrade applanga
```


## Initialize Project

To initialize a new project the API token is needed. It can be found in the App under **App Settings** on the [Applanga Dashboard](https://dashboard.applanga.com).

The project can then be initialized by running the following in the project directory:

```sh
	applanga init
```

In the appearing dialog project data like the API token and the type of project will be requested.
It will then save all the data to a configuration file into the current directory with the name `.applanga.json`


## Push & Pull Translation Files

The translations can simply be pushed to and pulled from Applanga with the corresponding commands.

To pull translations from Applanga into local files:

```sh
	applanga pull
```

###### *NOTE: The CLI is communicating with the [Applanga API](https://www.applanga.com/docs-integration/api) through our CDN to make sure the data is always reachable but that also means changes (including `push`es) are only available to pull after a 10 minute delay even though they are already visible on the [Dashboard](https://dashboard.applanga.com)!*

To push existing local translations to Applanga:

```sh
	applanga push
```

### Push Options

 - **--force**
 
By default values only get pushed if they aren't existing already on the dashboard to make sure not to accidentally overwrite translations. If you want to push local changed files you can do so with the `--force` option. But be cautios that this might overwrite values set ny a translator on the dashboard so be sure to pull before you push.

```sh
	applanga push --force
```

 - **--draft**
 
You can push values into that draft field to review them on the dashboard before you release them with the `--draft` option. 

```sh
	applanga push --draft
```



## Configuration

By default, the configuration file (`.applanga.json`) gets read from the current folder. It is however also possible to set an additional path to check for with the environment variable `APPLANGA_CONFIG`. If set it checks additionally also in its location.
Additionally. can the configuration file be located in the home folder set in the environment variable `HOME` under Linux/Mac and `HomePath` under Windows.


### Project Structure

The most basic configuration file generated after `applanga init` will look similar to this e.g. for a **.po** file:

```json
{
	"app": {
		"access_token": "5b1f..!..2ab",
		"base_language": "en", 
		"pull": {
			"target": [
				{
					"file_format": "gettext_po", 
					"path": "./<language>.po"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"file_format": "gettext_po", 
					"path": "./<language>.po"
				}
			]
		}
	}
}
```
If you are using multiple files, file formats on platforms that have different folders for their base languages or more complex folder structures like [iOS](#ios-configuration-examples) or [Android](#android-configuration-examples) you'll need to modify the config as show in the [configuration examples](#configuration-examples).

### Target/Source Properties


There are a few mandatory and several optional properties that you can use to customize the cli to match your specific project setup.

#### Mandatory Properties:

- **"file_format"**

	The file format specifies the format of the file that you want to **push** or **pull** wich typically depends on the platform that you are localizing.

	For a detailed format description check out the [Applanga File Format Documentation](https://www.applanga.com/docs/formats)
	
	Currently, the following formats are supported:

	 - android_xml : [Android XML ](https://www.applanga.com/docs/formats/android_xml) (.xml)
	 - angular_translate_json : [Angular Translate](https://www.applanga.com/docs/formats/angular_translate_json) (.json)
	 - chrome_i18n_json : [Chrome i18n](https://www.applanga.com/docs/formats/chrome_i18n_json) (.json)
	 - ember_i18n_json_module : [Ember i18n JSON Module](https://www.applanga.com/docs/formats/ember_i18n_json_module) (.js)
	 - ini : [INI](https://www.applanga.com/docs/formats/ini) (.ini)
	 - gettext_po : [Gettext PO File](https://www.applanga.com/docs/formats/gettext_po) (.po)
	 - gettext_pot : [Gettext POT File](https://www.applanga.com/docs/formats/gettext_pot) (.pot)
	 - go_i18n_json : [go-i18n](https://www.applanga.com/docs/formats/go_i18n_json) (.json)
	 - i18next_json : [i18next](https://www.applanga.com/docs/formats/i18next_json) (.json)
	 - ios_strings : [iOS strings](https://www.applanga.com/docs/formats/ios_strings) (.strings)
	 - ios_stringsdict : [iOS stringsdict](https://www.applanga.com/docs/formats/ios_stringsdict) (.stringsdict)
	 - java_properties : [JAVA properties](https://www.applanga.com/docs/formats/java_properties)(.properties)
	 - mozilla_i18n_json : [Mozilla i18n](https://www.applanga.com/docs/formats/mozilla_i18n_json) (.json)
	 - mozilla_properties : [Mozilla properties](https://www.applanga.com/docs/formats/mozilla_properties) (.properties)
	 - nested_json : [Nested JSON](https://www.applanga.com/docs/formats/nested_json)(.json)
	 - node_2_json : [i18n-node-2](https://www.applanga.com/docs/formats/node_2_json) (.json)
	 - react_nested_json : [React Nested JSON](https://www.applanga.com/docs/formats/react_nested_json) (.json)
	 - react_simple_json : [React Simple JSON](https://www.applanga.com/docs/formats/react_simple_json) (.json)
	 - ruby_on_rails_yaml : [Ruby on Rails YAML](https://www.applanga.com/docs/formats/ruby_on_rails_yaml) (.yaml)
	 - symfony_yaml : [Symfony YAML](https://www.applanga.com/docs/formats/symfony_yaml) (.yaml)
	 - symfony2_yaml : [Symfony 2 YAML](https://www.applanga.com/docs/formats/symfony2_yaml) (.yaml)
	 - arb : [Flutter](https://www.applanga.com/docs/formats) (.arb)
	 - laravel_php : [PHP Laravel](https://www.applanga.com/docs/formats) (.php)

	***Example:*** `"file_format": "android_xml"`

- **"path"**

	In the **"source"** block it defines the files to upload and in **"target"** block the files to download.
It is possible to set the variable `<language>` in the path. In the "source" block it will look for local files which have the language code set at its location (like: "en") and then upload the file for the found language. In "target" block it will replace it with the name of the languages which exist on Applanga and create the files accordingly.

	***Example:*** `"path": "./app/src/main/res/values-<language>/strings.xml"`

#### Optional Properties:

- **"tag"**

	Needed if you have multiple local files which is common on [iOS](#ios-app-with-pluralization-stringsdict-and-storyboard-strings) and [Android](#android-app-with-multiple-files-submodule-library). If defined in the **"source"** block it will set the specified tag to all strings that are uploaded from the given **"path"**. In the **"target"** block it will only download translations which have this tag applied.
	This is needed if you want to up and download only a subset of all available strings into or from certain files.

	***Example:*** `"tag": "main page"`

- **"language"**

	The language of the file. Is only needed if there is no placeholder `<language>` defined in "path" e.g. for your base **"./values/"** or **"./Base.lproj/"** folder.

	***Example:*** `"language": "en"`

- **"exclude_languages"**

	If you are using the placeholder `<language>` to download a file for all languages on the project it might be needed to exclude some languages from being pushed or pulled.

	***Example:*** `"exclude_languages": ["en", "de-AT"]`

- **"export_empty"** *(target only)*

	**pull** translations that are empty on the applanga dashboard which by default would get skipped. This property is only evaluated in the **"target"** block.
	This setting makes sense e.g. if you want the empty strings in your base language but not in the translations so they can fall back to the base strings or if you use the cli to pull files that you want to send to translators.

	***Example:*** `"export_empty": true`

# Configuration Examples
---
## Android Configuration Examples

### Basic Android App
The base Android strings are located in `./app/src/main/res/values/strings.xml`, other languages are located in `./app/src/main/res/values-<language>/strings.xml`. The following example shows the usage for a basic Android project with english set as base language.

```json
{
	"app": {
		"access_token": "5b1f..!..2ab", 
		"base_language": "en", 
		"pull": {
			"target": [
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"path": "./app/src/main/res/values-<language>/strings.xml"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "android_xml", 
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml", 
					"path": "./app/src/main/res/values-<language>/strings.xml"
				}
			]
		}
	}
}
```

### Android App with Multiple Files & Submodule / Library

Apps can have strings in multiple files or in shared libraries. You can specify multiple files in the`.applanga.json` but to be able to up and download the subset of strings to the correct file you need to use the **"tag"** property so that Applanga can properly identify them.

```json
{
	"app": {
		"access_token": "5b1f..!..2ab", 
		"base_language": "en", 
		"pull": {
			"target": [
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"tag": "Main App Strings",
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Main App Strings",
					"path": "./app/src/main/res/values-<language>/strings.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"tag": "Other App Strings",
					"path": "./app/src/main/res/values/other.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Other App Strings",
					"path": "./app/src/main/res/values-<language>/other.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"tag": "Main Library Strings", 
					"path": "./mylibrary/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Main Library Strings",
					"path": "./mylibrary/src/main/res/values-<language>/strings.xml"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "Main App Strings",
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Main App Strings",
					"path": "./app/src/main/res/values-<language>/strings.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "Other App Strings",
					"path": "./app/src/main/res/values/other.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Other App Strings",
					"path": "./app/src/main/res/values-<language>/other.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "Main Library Strings", 
					"path": "./mylibrary/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "Main Library Strings",
					"path": "./mylibrary/src/main/res/values-<language>/strings.xml"
				}
			]
		}
	}
}
```

## iOS Configuration Examples

### Basic iOS App
If Base Localization is enabled the base iOS strings are located in `./Base.lproj/Localizable.strings`, other languages are located in `./<language>.lproj/Localizable.strings`. The following example shows the usage for a basic iOS project with english set as base language.

```json
{
	"app": {
		"access_token": "5b1f..!..2ab", 
		"base_language": "en", 
		"pull": {
			"target": [
				{
					"language": "en",
					"file_format": "ios_strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"path": "./<language>.lproj/Localizable.strings"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "ios_strings", 
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings", 
					"path": "./<language>.lproj/Localizable.strings"
				}
			]
		}
	}
}
```

### iOS App with Pluralization .stringsdict and Storyboard .strings
If you turn on localization on your storyboards you will end up with a .strings file for every storyboard in every language and since strings on the Applanga dashboard are merged to one big list you need to use the config **"tag"** property to tag the strings for the specific files on **push** and **pull** so you can identify them later on.
To extract the .strings from your storyboard you can use the following command 

```sh
ibtool MainStoryboard.storyboard --generate-strings-file MainStoryboard.strings
```

For Pluralization apple introduced the [.stringsdict File Format](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/StringsdictFileFormat/StringsdictFileFormat.html) which you can also conveniently **push** and **pull** with the Applanga command line interface. A .stringsdict file always need an accompanying .strings file so you can use the same **tag** for both.

```json
{
	"app": {
		"access_token": "5b1f..!..2ab", 
		"base_language": "en", 
		"pull": {
			"target": [
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "Localizable.strings",
					"path": "./<language>.lproj/Localizable.strings"
				},
				{
					"language": "en",
					"file_format": "ios_stringsdict",
					"tag": "Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.stringsdict"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_stringsdict",
					"tag": "Localizable.strings",
					"path": "./<language>.lproj/Localizable.stringsdict"
				},
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "MainStoryboard.strings",
					"export_empty": true,
					"path": "./Base.lproj/MainStoryboard.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "MainStoryboard.strings",
					"path": "./<language>.lproj/MainStoryboard.strings"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "Localizable.strings",
					"path": "./<language>.lproj/Localizable.strings"
				},
				{
					"language": "en",
					"file_format": "ios_stringsdict",
					"tag": "Localizable.strings",
					"path": "./Base.lproj/Localizable.stringsdict"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_stringsdict",
					"tag": "Localizable.strings",
					"path": "./<language>.lproj/Localizable.stringsdict"
				},
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "MainStoryboard.strings",
					"path": "./Base.lproj/MainStoryboard.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "MainStoryboard.strings",
					"path": "./<language>.lproj/MainStoryboard.strings"
				}
			]
		}
	}
}
```
