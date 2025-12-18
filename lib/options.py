# lib/cli_utils.py
import click
from typing import List, Dict, Optional
import json
import re
from copy import deepcopy
from .constants import TAG_NAME_CHAR_LIMIT, DEBUG_TEXT_COLOR

def parse_and_validate_tags(tags_list):
    """
    Validates the list of tags passed in from CLI.

    Returns:
        (is_valid: bool, parsed_tags: list[str])
    """
    if not tags_list:
        return True, None

    parsed_tags = [tag for tag in tags_list if isinstance(tag, str) and tag != '']

    if not parsed_tags:
        click.echo('"--tag" must be provided as a non-empty strings')
        return False, None
    
    for tag in parsed_tags:
        if len(tag) > TAG_NAME_CHAR_LIMIT:
            click.echo(f'Tag name cannot be longer than {TAG_NAME_CHAR_LIMIT} characters.')
            return False, None

    return True, parsed_tags


def filter_files_by_tags(files: List[Dict], parsed_tags: Optional[List[str]]) -> List[Dict]:
    """
    Filters a list of file dictionaries based on the presence of matching tags.

    Each file may have a "tag" field, which can be a string or a list of strings.
    The file is included in the output if any of its tag values match one of the parsed_tags.

    Args:
        files: A list of file dictionaries, each possibly containing a "tag" field.
        parsed_tags: A list of tag strings to match against.

    Returns:
        A filtered list of files where the "tag" field contains at least one matching tag.
        If parsed_tags is None or empty, the original files list is returned unchanged.

    Side effect:
        Logs an error if any of the provided tags did not match any file tag.
    """
    if not parsed_tags:
        return files

    parsed_tags_set = set(parsed_tags)
    filtered_files: List[Dict] = []
    matched_tags = set()

    for file in files:
        tag_field = file.get('tag')

        if isinstance(tag_field, str):
            # Simple tag comparison
            if tag_field in parsed_tags_set:
                filtered_files.append(file)
                matched_tags.add(tag_field)

        elif isinstance(tag_field, list):
            # Compare all string items in list
            match_found = False
            for t in tag_field:
                if isinstance(t, str) and t in parsed_tags_set:
                    matched_tags.add(t)
                    match_found = True
            if match_found:
                filtered_files.append(file)

        # Ignore entries with missing or unsupported tag types silently 

    # Log any requested tags that didn’t match any file
    unmatched = [t for t in parsed_tags if t not in matched_tags]
    if unmatched:
        click.secho(
            'No files matched for the following --tag values: ' + ', '.join(unmatched),
            err=True,
            fg='red'
        )

    return filtered_files



def validate_tags_length_in_files(files: List[Dict]) -> bool:
    """
    Validates the length of tags within a list of files.

    This will be used if no tag is provided via cli.
    """
    for file_config in files:
        if 'tag' in file_config:
            tags_to_check = file_config['tag']
            
            # create a tag list in case of one tag
            if not isinstance(tags_to_check, list):
                tags_to_check = [tags_to_check]

            # check tag length
            for tag in tags_to_check:
                if len(str(tag)) > TAG_NAME_CHAR_LIMIT:
                    click.secho(f'Tag name cannot be longer than {TAG_NAME_CHAR_LIMIT} characters. Check the config file!', fg='red')
                    return False
    return True



def log_config(ctx, config_file_data):
    """
    Logs the applanga config (sanitized) in DEBUG mode.
    - Removes app.access_token before logging.

    This function is no-op when DEBUG is falsy.
    """

    if not ctx.obj['DEBUG']:
        return

    try:
        # Make a safe copy, then redact token without mutating the original
        safe = deepcopy(config_file_data)
        if isinstance(safe, dict) and isinstance(safe.get('app'), dict):
            # Remove token if present
            safe['app'].pop('access_token', None)

        click.secho('Applanga Config:', fg=DEBUG_TEXT_COLOR)
        click.secho(
            json.dumps(safe, ensure_ascii=False, indent=2),
            fg=DEBUG_TEXT_COLOR
        )

    except Exception as e:
        click.secho('Failed to log config file: %s' % str(e), err=True, fg='red')



LANGUAGE_CODE_PATTERNS = [
    re.compile(r'^[a-z]{2}(-[A-Z][a-z]{3})?(-[A-Z]{2})?$'),
    re.compile(r'^[a-z]{3}$')
]


def language_code_is_valid(code):
    """
    Validate a language code. Return True if the given language code matches one of the supported formats.

    Supported formats include:
      - "en", "fr", "de"                  (2-letter ISO 639-1)
      - "aaa", "aar"                      (3-letter ISO 639-2/3)
      - "en-US", "de-DE"                  (language-REGION)
      - "zh-Hant-TW", "sr-Cyrl-RS"        (language-Script-REGION)

    Examples of invalid codes:
      - "EN"          (must be lowercase)
      - "en-us"       (region must be uppercase)
      - "en_latn_US"  (wrong separators)
      - "engl"        (too long, not ISO format)
    """
    return any(regex.match(code) for regex in LANGUAGE_CODE_PATTERNS)


def parse_and_validate_languages(languages):
    """Parse the --languages option and validate each code."""
    if not languages:
        return True, []

    parsed = [code.strip() for code in languages.split(',') if code.strip()]

    invalid = [code for code in parsed if not language_code_is_valid(code)]

    if invalid:
        click.secho(
            'Invalid language code(s): %s' % ', '.join(invalid),
            err=True,
            fg='red'
        )
        return False, []

    return True, parsed
