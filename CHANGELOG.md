# Applanga Localization Command Line Interface CHANGELOG
***
*Website:* <https://www.applanga.com>

*Applanga CLI Documentation:* <https://www.applanga.com/docs-integration/cli>
***

### Version 1.0.116 (18 Dec 2025)
#### Added
- Added `--languages` flag to `pull` command
---

### Version 1.0.114 (3 Nov 2025)
#### Added
- Added max length check for Tags (400 Characters)
- Fixed a misleading error message about internet connection and invalid token
- Added debug logs for unknown tags given via `--tag` option
---

### Version 1.0.113 (7 Aug 2025)
#### Added
- Added `tag_category` option
- Added `--tag` option to `push`, `pushtarget`, `pull`, and `pullsource` commands for filtering files or entries by tag
---

### Version 1.0.112 (17 Jul 2025)
#### Added
- Added `autoGenerateMissingKeys` option for `csv`, `tsv` and `xls` formats
---

### Version 1.0.111 (17 Jun 2025)
#### Added
- Added `disable-cert-verification` option to disable certificate verification
#### Fixed
- Error handling for certain requests
---

### Version 1.0.110 (5 Jun 2025)
#### Fixed
- Fixed an issue with the `columnDescription` option with `<language>` placeholder in use
- Adapted the documentation for the `excludeHeaderRow` option to be more clear
---

### Version 1.0.106 (27 Mar 2025)
#### Added
- Added `skipNonStringValues` option for json formats
---

### Version 1.0.105 (20 Feb 2025)
#### Added
- Added `csv`, `tsv` and `xls` file formats
---

### Version 1.0.104 (19 Dez 2024)
#### Fixed
- Added improved contradictory configuration error 
- Fixed init script for windows file path conversion
---

### Version 1.0.103 (10 Dez 2024)
#### Fixed
- Fixed contradictory configurations error messages for ios / ios_stringsdict overlap
---

### Version 1.0.102 (21 Nov 2024)
#### Fixed
- Fixed initialize script and documentation for android / ios default setup
---

### Version 1.0.101 (5 Nov 2024)
#### Fixed
- Added error messages for contradictory configurations
---

### Version 1.0.93 (18 Apr 2024)
#### Fixed
- Fixed keepTagIds option for push commands
---

### Version 1.0.92 (4 Jan 2024)
#### Added
- Added `xliff` file format
- Added `X-Integration` header
---

### Version 1.0.91 (7 Dec 2023)
#### Added
- Added `remove_cr_char` option
---

### Version 1.0.89 (7 Aug 2023)
#### Added
- Improved pull command to retrieve localization changes immediately
---

### Version 1.0.86 (7 Jul 2023)
#### Added
- Added `branch_id` description to the Documenation
---

### Version 1.0.83 (9 Jun 2023)
#### Added
- Added `sort_by_key` option
---

### Version 1.0.78 (25 May 2023)
- Added missing File formats to the Documentation
---

### Version 1.0.77 (8 Dec 2022)
#### Added
- Improved init script to include 'tag' option by default
---

### Version 1.0.76 (29 Nov 2022)
#### Added
- Added `key_prefix` option
---

### Version 1.0.75 (13 Jun 2022)
#### Fixed
- Fixed documentation to include the new includeInvisibleId command option
---

### Version 1.0.74 (17 Mar 2022)
#### Added
- added new command `updateSettingsfiles`
---

### Version 1.0.73 (10 Mar 2022)
#### Added
- Added includeInvisibleId option for pull command
---

### Version 1.0.72 (17 Dec 2021)
#### Added
- Improved error messages for certain configuration files
- Added keepTagIds option for push command
- Modified default configuration from the init script
- Added pullsource and pushtarget command
---

### Version 1.0.70 (12 Oct 2021)
#### Added
- Added Pull option `convert_placeholder` to support converting string formatters or placeholder between IOS to Android or viceversa. See Readme documentation for more information.
- Added includeMetadata option for pull command
---

### Version 1.0.68 (2 Sep 2021)
#### Added
- Added installation instructions for the CLI for pre macOS 11 systems
- Improved error messages for multiple complex errors
---

### Version 1.0.67 (1 Jul 2021)
#### Added
- Added Push / Pull language mappings for <language> selector
- Added support for configurations which only provide either a push or pull block
- Support for specifying an Array of tags for the push/pull command
---

### Version 1.0.65 (21 May 2021)
#### Added
- Support for Qt Linguist files (.ts)
- added 'disable plurals' configuration option for .yaml, ember-i18n and node-2 .json formats
---

### Version 1.0.51 (13 Jan 2021)
#### Added
- option `disable_plurals` support in `.applanga.json` file. Used to disable plural when `applanga push` or `applanga pull` is executed for `nested_json` and `react_nested_json` file formats.
- `ignore_duplicates` option support `.applanga.json` file, which when set will ignore duplicate keys when `applanga pull` is executed.
---

### Version 1.0.49 (18 Jun 2020)
#### Added
- made underscore locale folder support more generic as if a folder with a _ language code exists but non with - use the _ for `applanga pull` and for `push` both variants can be pushed

---
### Version 1.0.48 (16 Jun 2020)
#### Fixed
- fixed arb files will use locales with _ instead of - if a region suffix is present

---
### Version 1.0.47 (28 May 2020)
#### Fixed
- fixed RequestsDependencyWarning: urllib3 or chardet doesn't match a supported version!

---
### Version 1.0.46 (28 May 2020)
#### Fixed
- fixed FileNotFoundError on Python 2

---
### Version 1.0.45 (28 Feb 2020)
#### Added
- option to provide `access_token` as environment variable

---
### Version 1.0.44 (13 Feb 2020)
#### Added
- Support for Flutter .arb files
- Support for Laravel .php files
- Automatic `r` prefix for android locale region directories with `<language>` wildcard
- Setup proper base language folders for iOS and Android default config
- (optional) provide base language folder as command line parameter

---
### Version 1.0.43 (7 Nov 2018)
#### Added
- Support for pushing changed local strings with the --force option
- Support for pushing strings as draft with the --draft option

---
### Version 1.0.42 (28 Aug 2018)
#### Added
- Support for ini file localization

---
### Version 1.0.41 (8 Aug 2018)
#### Added
- Support for chrome i18n json localization
- Support for go i18n json localization
- Support for mozilla i18n json localization
- Support for Mozilla .properties localization
- Support for Java .properties localization
- download empty values
- extended documentation

---
### Version 1.0.39 (17 Jul 2018)
#### Added
- Support for angular translate json
- Support for 18n-node2 json
- Support for i18next json

---
### Version 1.0.37 (10 Jul 2018)
#### Fixed
- Linux ssl/tls version

---
#### Added
- Support for poeditor .po & .pot files
- Support for microsft .NET .resw & .resx files

---
### Version 1.0.34 (3 Jul 2018)
#### Fixed
- do not download empty strings

#### Added
- option to overwrite values on push

---
### Version 1.0.32 (26 Jun 2018)
#### Added
- added links to cli on applanga website and other doc updates

---
### Version 1.0.30 (22 Jun 2018)
#### Added
- homebrew doc update

---
### Version 1.0.29 (22 Jun 2018)
#### Added
- added installation instructions and homebrew support

---
### Version 1.0.26 (19 Jun 2018)
#### Added
- documentation update

---
### Version 1.0.0 (19 Jun 2018)
#### Added
- up and download of android and ios strings
