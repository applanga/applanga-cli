# Applanga Localization Command Line Interface (CLI)

***
*Version:* 1.0.84

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

###### Installing on Mac pre MacOS 11
Please note that in order to run the latest Applanga CLI version on macOS you need to have at least macOS 11 (Big Sur) installed. If you are stuck with an older macOS you can use [Applanga CLI 1.0.84](https://github.com/applanga/applanga-cli/releases/tag/1.0.51) but be aware that not all features and fixes are available in that version. Please check the [Applanga CLI 1.0.51 README](https://github.com/applanga/applanga-cli/blob/1.0.51/README.md) and [CHANGELOG](https://www.applanga.com/changelog/cli) for more details.

In order to install this via brew you need to run:
	
```sh
	brew tap applanga/cli
	brew install applanga@1.0.84
```

##### Github

To automate localization through Github please check the [Applanga Github Workflow Documentation](https://www.applanga.com/docs/integration-documentation/github-action).

## Initialize Project

To initialize a new project the API token is needed. It can be found in the App under **Project Settings** on the [Applanga Dashboard](https://dashboard.applanga.com).

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

The default config usually just pushes the source language and pull's all target languages. For some initial setup cases it might be needed to Push Target values as well. For this there is the **pushtarget** command. It behaves the same as the push command but pushes all files that are set as targets in the config. If you want to override already existing translations on the backend you’ll need to combine this with the --force command

```sh
	applanga pushtarget
```

For cases where you need to pull the source language changes from the dashboard into your source file you can use the **pullsource** command. It behaves the same as a pull but only pulls source files. Please be aware that local changes that are not yet pushed to Applanga will be overwritten.

```sh
	applanga pullsource
```



### Push Options

 - **--force**
 
By default values only get pushed if they aren't existing already on the dashboard to make sure not to accidentally overwrite translations. If you want to push local changed files you can do so with the `--force` option. But be cautios that this might overwrite values set by a translator on the dashboard, so be sure to pull before you push.

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
If you do not want to have your `access_token` token stored in the config and commited to your scm you can remove it from the config and instead provide it as environment variable called `APPLANGA_ACCESS_TOKEN`.


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
					"exclude_languages": ["en"],
					"file_format": "gettext_po", 
					"path": "./<language>.po",
					"tag": "app:language.po"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "gettext_po", 
					"path": "./en.po",
					"tag": "app:language.po"
				}
			]
		}
	}
}
```
If you are using multiple files, file formats on platforms that have different folders for their base languages or more complex folder structures like [iOS](#ios-configuration-examples) or [Android](#android-configuration-examples) you'll need to modify the config as shown in the [configuration examples](#configuration-examples).

### Target/Source Properties


There are a few mandatory and several optional properties that you can use to customize the cli to match your specific project setup.

#### Mandatory Properties:

- **"file_format"**

	The file format specifies the format of the file that you want to **push** or **pull** which typically depends on the platform that you are localizing.

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
	 - arb : [Flutter](https://www.applanga.com/docs/formats/arb) (.arb)
	 - laravel_php : [PHP Laravel](https://www.applanga.com/docs/formats/laravel_php) (.php)
	 - qt_ts : [Qt Linguist](https://www.applanga.com/docs/formats/ts) (.ts)
	 - microsoft_resw: [Microsoft Resw](https://www.applanga.com/docs/formats/microsoft_resx) (.resw)
	 - microsoft_resx: [Microsoft Resx](https://www.applanga.com/docs/formats/microsoft_resx) (.resx)
	 - toml : [Toml](https://www.applanga.com/docs/formats/toml) (.toml)

	***Example:*** `"file_format": "android_xml"`

- **"path"**

	In the **"source"** block it defines the files to upload and in **"target"** block the files to download.
It is possible to set the variable `<language>` in the path. In the "source" block it will look for local files which have the language code set at its location (like: "en") and then upload the file for the found language. In "target" block it will replace it with the name of the languages which exist on Applanga and create the files accordingly.

	***Example:*** `"path": "./app/src/main/res/values-<language>/strings.xml"`

#### Optional Properties:

- **"branch_id"**:
	
	Defines the branch to use for the configuration. If not set the default branch will be used. This will only work for Projects, where branching is enabled. You can read find out the branch id in the Project settings.

	To learn more about branching please have a look [here](www.applanga.com/docs/advanced-features/branching)

	***Example:*** `"branch_id": "<branch_id>"`


- **"tag"**

	Needed if you have multiple local files which is common on [iOS](#ios-app-with-pluralization-stringsdict-and-storyboard-strings) and [Android](#android-app-with-multiple-files-submodule-library). If defined in the **"source"** block it will set the specified tag to all strings that are uploaded from the given **"path"**. In the **"target"** block it will only download translations which have this tag applied.
	This is needed if you want to up and download only a subset of all available strings into or from certain files. In addition to a single tag you can also provide an array if you want to **pull** elements that are tagged differently into one file or if you want to add multiple tags for certain files on **push**.
	
	**Warning**: 
	
	If you’re pushing the same file in multiple languages you need to make sure that all of them contain the same keys or some Tags will get deleted or mixed up.
	
	All related plurals must be included in the uploaded file to ensure they share an identical tag. This includes adding all plural forms required by other languages even if the uploaded language does not use those forms. This ensures that all plurals are tagged appropriately and exported across languages.
	
	***Example (Single Tag):*** `"tag": "main page"`
	
	***Example (Tag Array):*** `"tag": ["main page", "other page"]`


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

- **"disable_plurals"**
	
	This option is only supported when `file_format` is set to `nested_json`, `react_nested_json`, `ruby_on_rails_yaml`, `symfony_yaml`, `symfony2_yaml`, `ember_i18n_json_module` or `node_2_json`. It can be set to `true` or `false`. When set to `true` it means plural keys (`'zero', 'one', 'two', 'few', 'many', 'other'`) will be handled as regular keys and will not undergo any special transformation. For example if this option is set to `true` when `applange push` is executed for a `nested_json` file that contains the following content

	```json
	{
		"some": {
			"sub": {
				"other": "foo"
			}
		}
	}
	``` 

	when the operation completes the resulting string key will be `some.sub.other` instead of `some.sub[other]`. Then for 
	`applanga pull`, if `disable_plural` is set to `true` then keys like `some.sub[other]` with value as `foo` will become

	```json
	{
		"some.sub[other]": "foo"
	}
	``` 

	instead of 

	```json
	{
		"some": {
			"sub": {
				"other": "foo"
			}
		}
	}
	```

	***Example:*** `"disable_plural": true`

- **"ignore_duplicates"** *(target only)*

	This option if set to `true`, the cli will skip duplicate keys whenever `applanga pull` is executed. For instance if we have keys and values as follows `test = “teststring”`, `test.sub1 = “subteststring1“` and `test.sub2 = “subteststring2“` when we try to pull files then the key `test = “teststring"` and its value will be excluded from the imported file if this option is set to `true`. But when set to `false` the pull operation will fail and the cli will log an error to console stating which keys conflict.

	***Example:*** `"ignore_duplicates": true`


- **"languageMapping"**

	If you use the `<language>` wildcard this option allows to specify a map from Applanga language names to different language names that you use in your folders or filenames locally. The example below maps “nb-NO” which is the language name as its defined on the Applanga dashboard to “no_NO” in a local project.

	***Example:***
	```json
	"languageMap": {
		"nb-NO": "no_NO",
		"zh-Hans": "zh_CN"
	}
	```
	
- **"includeMetadata"** *(target only)*

	This option is by default set to `true`, if false metadata information will be excluded from the given target.

	***Example:*** `"includeMetadata": false`
	
- **"includeInvisibleId"**  *(target only)*

	This option is by default set to `false`, if true an invisible Id will be added in front of each translation value. The invisible Id consists of zero width invisible unicode characters to not mess up the look of your application. This allows us to enable additional features like for example a live web view of your application. 
	
	This should only be used in your application during the development process not in production settings.

- **"convert_placeholder"**

	If you use the string formatter or placeholder in your strings, as part of your project, you can use this option to convert the placeholders between iOS and Android platforms. If convert_placeholder is set to `true`, the CLI will convert and export your string whenever `applanga pull` is executed. For example, if you have a project in IOS where your string is `"Hello %@"` use convert_placeholder key to convert it to the Android format `"Hello %s"`.

	***Example:*** `"convert_placeholder": true`

	Convert placeholder works in conjunction with "file_format" key. To generate the file and convert from iOS to Android must be specified "android_xml" and to change from Android to iOS must be "ios_strings" or "ios_stringsdict".


	***Example:*** 
	
	iOS to Android: 	`"file_format":"android_xml"`

	Android to iOS:  `"file_format":"ios_strings"`



	***iOS to Android conversion rules***
	- Length format is converted to  "%d".

	- Unsupported conversion types by default will converted to "%s".

	- Float "%f", double "%g"  and "%p" are converted to "%d".

	- All Instances of "%@" will converted to "%s".
	
	- Positional Arguments "%1$@" will be converted to "%1$s"

	- Objective C integer types like "%i" and "%u" are converted to "%d".

	- If it is the same pattern, it will keep the original.  

	***Android to iOS conversion rules***

	- Unsupported conversion types will convert to default "%@" type.

	- Date/Time conversion types like "%1$te" will convert to "%1$@"

	- Positional Arguments "%1$s" will be converted to "%1$@"
	
	- Relative positional arguments like "%1$s %<s" will be converted to "%1$@ %1$@"

	- All instances of "%s" will be converted to "%@".

	- If it is the same pattern, will keep the original.  

- **"key_prefix"**

	If you need to import multiple files with similar keys but different text, the option allows to add prefixes to the keys on import and remove prefixes on export.

	**Note**: 

	The `key_prefix` text property cannot be longer than 50 characters and can only contains letters, numbers, space, undescore and dash. 

	***Example:*** `"key_prefix": "added_prefix1-"`

- **"sort_by_key"** *(target only)*

	The the keys in files downloaded on **pull** command are sorted alphabetically. This property is only evaluated in the **"target"** block. This option is by default set to `false`.

	***Example:*** `"sort_by_key": true`
	
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
					"path": "./app/src/main/res/values/strings.xml",
					"tag": "app:strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"path": "./app/src/main/res/values-<language>/strings.xml",
					"tag": "app:strings.xml"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "android_xml", 
					"path": "./app/src/main/res/values/strings.xml",
					"tag": "app:strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml", 
					"path": "./app/src/main/res/values-<language>/strings.xml",
					"tag": "app:strings.xml"
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
					"tag": "app:strings.xml",
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "app:strings.xml",
					"path": "./app/src/main/res/values-<language>/strings.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"tag": "app:other.xml",
					"path": "./app/src/main/res/values/other.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "module:other.xml",
					"path": "./app/src/main/res/values-<language>/other.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"export_empty": true,
					"tag": "module:strings.xml", 
					"path": "./mylibrary/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "module:strings.xml",
					"path": "./mylibrary/src/main/res/values-<language>/strings.xml"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "app:strings.xml",
					"path": "./app/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "app:strings.xml",
					"path": "./app/src/main/res/values-<language>/strings.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "app:other.xml",
					"path": "./app/src/main/res/values/other.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "app:other.xml",
					"path": "./app/src/main/res/values-<language>/other.xml"
				},
				{
					"language": "en",
					"file_format": "android_xml",
					"tag": "module:strings.xml", 
					"path": "./mylibrary/src/main/res/values/strings.xml"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "android_xml",
					"tag": "module:strings.xml",
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
					"path": "./Base.lproj/Localizable.strings",
					"tag": "app:Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"path": "./<language>.lproj/Localizable.strings",
					"tag": "app:Localizable.strings"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "ios_strings", 
					"path": "./Base.lproj/Localizable.strings",
					"tag": "app:Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings", 
					"path": "./<language>.lproj/Localizable.strings",
					"tag": "app:Localizable.strings"
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
					"tag": "app:Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "app:Localizable.strings",
					"path": "./<language>.lproj/Localizable.strings"
				},
				{
					"language": "en",
					"file_format": "ios_stringsdict",
					"tag": "app:Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.stringsdict"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_stringsdict",
					"tag": "app:Localizable.strings",
					"path": "./<language>.lproj/Localizable.stringsdict"
				},
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "storyboard:Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/MainStoryboard.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "storyboard:Localizable.strings",
					"path": "./<language>.lproj/MainStoryboard.strings"
				}
			]
		}, 
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "app:Localizable.strings",
					"export_empty": true,
					"path": "./Base.lproj/Localizable.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "app:Localizable.strings",
					"path": "./<language>.lproj/Localizable.strings"
				},
				{
					"language": "en",
					"file_format": "ios_stringsdict",
					"tag": "app:Localizable.strings",
					"path": "./Base.lproj/Localizable.stringsdict"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_stringsdict",
					"tag": "app:Localizable.strings",
					"path": "./<language>.lproj/Localizable.stringsdict"
				},
				{
					"language": "en",
					"file_format": "ios_strings",
					"tag": "storyboard:Localizable.strings",
					"path": "./Base.lproj/MainStoryboard.strings"
				},
				{
					"exclude_languages": ["en"],
					"file_format": "ios_strings",
					"tag": "storyboard:Localizable.strings",
					"path": "./<language>.lproj/MainStoryboard.strings"
				}
			]
		}
	}
}
```

## Update Applanga Settings File

To update Applanga Settings File within a project, simply execute the following command:

```sh
	applanga updateSettingsfiles
```

The above command will recursively check and update any Applanga Settings File if there are new versions found.

### Php Laravel App with language mapping
The following example shows the usage for a basic Laravel project with english set as base language. Note that Laravel uses a different Pattern for [short keys](https://laravel.com/docs/8.x/localization#using-short-keys) than Applanga. In order to circumvent this issue a custom language mapping is set via the **languageMap** key


```json
{
	"app": {
		"access_token": "5b1f..!..2ab",
		"base_language": "en",
		"pull": {
			"target": [
				{
					"exclude_languages": ["en"],
					"file_format": "laravel_php",
					"path": "./<language>.php",
					"tag": "app:language.php"
				}
			]
		},
		"push": {
			"source": [
				{
					"language": "en",
					"file_format": "laravel_php",
					"path": "./en.php",
					"tag": "app:language.php"
				}
			]
		}
	},
	"languageMap": {
		"nb-NO": "no_NO",
		"zh-Hans": "zh_CN"
	}
}
```
