# Applanga Localization Command Line Interface (CLI)

***
*Version:* 1.0.39

*Website:* <https://www.applanga.com>

*Changelog:* <https://www.applanga.com/changelog/cli>
***

## Table of Contents

  1. [Installation](#installation)
  2. [Initialization](#initialize-project)
  3. [Usage](#push-pull-translations)
  4. [Configuration](#configuration)


## Installation

##### Manual

1. [Download and extract](https://github.com/applanga/applanga-cli/releases/latest) the latest client binary for your platform.

2. Store the binary at a location where it can be found and executed by the system or adjust your [PATH](https://en.wikipedia.org/wiki/PATH_(variable)) accordingly

3. You should now be able to execute it on the commandline like:

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

To push existing local translations to Applanga:

```sh
	applanga push
```

To pull translations from Applanga into local files:

```sh
	applanga pull
```


## Configuration

By default, the configuration file (`.applanga.json`) gets read from the current folder. It is however also possible to set an additional path to check for with the environment variable `APPLANGA_CONFIG`. If set it checks additionally also in its location.
Additionally. can the configuration file be located in the home folder set in the environment variable `HOME` under Linux/Mac and `HomePath` under Windows.


#### Custom Project Structure

In case the project uses a custom structure the configuration file `.applanga.json` can get edited manually.

The most basic configuration file for Android will look like this:

```json
{
  "app": {
    "access_token": "5b1f....2ab",
    "base_language": "en",
    "push": {
      "source": [
        {
          "file_format": "android_xml",
          "path": "./res/values-<language>/strings.xml"
        }
      ]
    },
    "pull": {
      "target": [
        {
          "file_format": "android_xml",
          "path": "./res/values-<language>/strings.xml"
        }
      ]
    },
  }
}
```

It should only be needed to make changes in "target" and "source". Both have the same properties:

#### Target/Source Properties

 - file_format: The format the files are in
 - path: The path to the files
 - tag: Name of the tag to apply when pushing or to export on pull
 - language : The language of the file


##### file_format

Currently, the following formats are supported:

 - android_xml : Android XML (.xml)
 - angular_translate_json : [i18next](https://github.com/angular-translate/angular-translate) (.json)
 - gettext_po : Gettext PO File (.po)
 - gettext_pot : Gettext POT File (.pot)
 - i18next_json : [i18next](https://github.com/i18next/i18next) (.json)
 - ios_strings : iOS strings (.strings)
 - ios_stringsdict : iOS stringsdict (.stringsdict)
 - node_2_json : [i18n-node-2](https://github.com/jeresig/i18n-node-2) (.json)

*Example: "android_xml"*


##### path

In the "source" block it defines the files to upload and in "target" block the files to download.
It is possible to set the variable `<language>` in the path. In the "source" block it will look for local files which have the language code set at its location (like: "en") and then upload the file for the found language. In "target" block it will replace it with the name of the languages which exist on Applanga and create the files accordingly.

*Example: "./res/values-<language>/strings.xml"*


##### tag (optional)

Name of tag to use. If defined in the "source" block it will apply the tag to all translations uploaded. In the "target" block it will only download translations which have this tag applied.

*Example: "main page"*


##### language (optional)

The language of the file. Is only needed if there is no placeholder `<language>` defined in "path" e.g. for your base **"./values/"** or **"./Base.lproj/"** folder.

*Example: "en"*


##### exclude_languages (optional)

Excludes languages from being pushed or pulled.

*Example: ["en", "de-AT"]*
