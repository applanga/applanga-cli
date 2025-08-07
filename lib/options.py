# lib/cli_utils.py
import click
from typing import List, Dict, Optional

def parse_and_validate_tags(tags_list):
    """
    Validates the list of tags passed in from CLI.

    Returns:
        (is_valid: bool, parsed_tags: list[str])
    """
    if not tags_list:
        return True, None

    parsed_tags = [tag.strip() for tag in tags_list if isinstance(tag, str) and tag.strip()]

    if not parsed_tags:
        click.echo('"--tag" must be provided as a non-empty strings')
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
    """
    if not parsed_tags:
        return files

    parsed_tags_set = set(parsed_tags)
    filtered_files = []

    for file in files:
        tag_field = file.get('tag')

        if isinstance(tag_field, str):
            if tag_field in parsed_tags_set:
                filtered_files.append(file)
        elif isinstance(tag_field, list):
            if any(tag in parsed_tags_set for tag in tag_field):
                filtered_files.append(file)
        # Skip entries with missing or unexpected "tag" types

    return filtered_files
