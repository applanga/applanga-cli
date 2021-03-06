# Applanga Localization Command Line Interface CHANGELOG
***
*Website:* <https://www.applanga.com>

*Applanga CLI Documentation:* <https://www.applanga.com/docs-integration/cli>
***

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
