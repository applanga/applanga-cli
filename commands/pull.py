import click
import requests
import json

from lib import api
from lib import config_file
from lib import output
from lib import options


def filter_request_languages_for_target(
    request_languages,
    parsed_languages,
    exclude_languages,
    all_app_languages,
    target
):
    """
    Filter the list of request_languages for a given target based on:

      - request_languages: languages determined from config, <language> placeholder, or explicit language field
      - parsed_languages: languages provided by the --languages CLI option
      - exclude_languages: languages that should be excluded for this target (from config)
      - all_app_languages: all languages defined in the project (from API)
      - target: the current target configuration dict

    Any language that has an issue in one of the following categories will be logged
    and excluded from the final result:

      - missing_in_project: requested via --languages but not part of the project
      - excluded_requested: requested via --languages but listed in exclude_languages
      - missing_due_to_fixed_target: requested via --languages and part of the project,
        but ignored because the target is configured for a specific single language.
    """
    parsed_set = set(parsed_languages)
    exclude_set = set(exclude_languages) if exclude_languages else set()

    missing_in_project = []
    excluded_requested = []
    missing_due_to_fixed_target = []

    target_language = target.get('language', None)
    for language_code in parsed_languages:
        # Languages requested via --languages but not part of the project
        if language_code not in all_app_languages:
            missing_in_project.append(language_code)

        # Languages requested via --languages but excluded for this target
        if language_code in exclude_set:
            excluded_requested.append(language_code)

        # Languages requested via --languages but ignored due to a fixed language in target
        if target_language is not None and language_code != target_language:
            missing_due_to_fixed_target.append(language_code)

    # Logging of all issues
    if missing_in_project:
        click.secho(
            'The following languages were not found in this project and will be ignored for this target: %s'
            % ', '.join(sorted(missing_in_project)),
            err=True,
            fg='yellow'
        )
        click.secho(
            'Target configuration: %s'
            % json.dumps(target, indent=2),
            err=True,
            fg='yellow'
        )

    if excluded_requested:
        click.secho(
            'The following languages were requested but are excluded for this target: %s'
            % ', '.join(sorted(excluded_requested)),
            err=True,
            fg='yellow'
        )
        click.secho(
            'Target configuration: %s'
            % json.dumps(target, indent=2),
            err=True,
            fg='yellow'
        )

    if missing_due_to_fixed_target:
        click.secho(
            'The following requested languages are ignored because this target is configured for a specific language only: %s'
            % ', '.join(sorted(missing_due_to_fixed_target)),
            err=True,
            fg='yellow'
        )
        click.secho(
            'Target configuration: %s'
            % json.dumps(target, indent=2),
            err=True,
            fg='yellow'
        )

    # Any of these languages must be removed from the final output
    problematic_languages = set(
        missing_in_project + excluded_requested + missing_due_to_fixed_target
    )

    # Final filtered languages (only those allowed + requested + not problematic)
    filtered_languages = [
        language_code
        for language_code in request_languages
        if language_code in parsed_set and language_code not in problematic_languages
    ]

    return filtered_languages



@click.command()
@click.pass_context
@click.option(
    '--tag',
    'tags',
    multiple=True,
    help='Only pull entries with the specified tags. Can be specified multiple times, e.g. --tag login --tag error'
)
@click.option(
    '--languages',
    'languages',
    default='',
    help='Comma separated list of language codes to limit pulled entries (e.g. "en,de-DE").'
)
def pull(ctx, tags, languages):
    output.showCommandHeader('pull', ctx)

    # Tag parsing
    tags_valid, parsed_tags = options.parse_and_validate_tags(tags)
    if not tags_valid:
        return

    # Language parsing
    languages_valid, parsed_languages = options.parse_and_validate_languages(languages)
    if not languages_valid:
        return

    try:
        config_file_data = config_file.readRaw()

        if 'pull' not in config_file_data['app']:
            click.echo('In order to Pull you need to have a pull configuration set in your config file')
            return
    except config_file.ApplangaConfigFileNotValidException as e:
        click.secho('There was a problem with the config file:\n%s\n' % str(e), err=True, fg='red')
        return

    options.log_config(ctx, config_file_data)

    try:
        projectVersion = api.getProjectVersion(ctx)
    except api.ApplangaConnectionException as e:
        click.secho(str(e), err=True, fg='red')
        return
    except api.ApplangaRequestException as e:
        click.echo(str(e))
        return

    all_app_languages = []
    for target in config_file_data['app']['pull']['target']:
        if 'language' not in target:
            if '<language>' not in target['path']:
                # If also no placeholder is defined then there is no need to
                # query languages from API
                continue

            try:
                all_app_languages = api.getAllAppLanguages(ctx, projectVersion)
            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem getting the app languages:\n%s\n' % str(e), err=True, fg='red')
                return

            break
    target_files = config_file_data['app']['pull']['target']

    # Filter if parsed_tags is set
    if parsed_tags:
        try:
            target_files = options.filter_files_by_tags(target_files, parsed_tags)
        except Exception as e:
            click.secho('There was a problem while filtering target files by tags:\n%s\n' % str(e), err=True, fg='red')
            return
    else:
         # check 400 chars limit for tag names
        if not options.validate_tags_length_in_files(target_files):
            return

    for target in target_files:

        if 'language' in target:
            # Language is defined in config
            request_languages = [target['language']]
        elif '<language>' in target['path']:
            # Language placeholder is defined in path so download all languages
            request_languages = list(all_app_languages)
        else:
            # No language defined so error
            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], 'missing'))
            click.echo('=' * 60)
            click.echo('Result: "Error"')
            click.secho(
                'You either need to use the <language> wildcard inside the path string or '
                'set it explicitly per file via the "language" property.\n',
                err=True,
                fg='red'
            )
            continue

        # Remove all the languages on the exclude list
        exclude_languages = []
        if 'exclude_languages' in target:
            exclude_languages = target['exclude_languages']

        request_languages = [x for x in request_languages if x not in exclude_languages]

        # Apply parsed_languages filter if provided
        if parsed_languages:
            request_languages = filter_request_languages_for_target(
                request_languages,
                parsed_languages,
                exclude_languages,
                all_app_languages,
                target
            )

        # Skip if nothing left
        if not request_languages:
            continue

        target['projectVersion'] = projectVersion

        # Go through all the languages that should be downloaded
        for language in request_languages:
            target['language'] = language

            click.echo('\nDownload :  %s\nLanguage :  %s' % (target['path'], language))
            click.echo('=' * 60)

            try:
                file_written = api.downloadFile(ctx, target)
                click.echo('Result: "Success"')
                click.echo('Wrote file: %s' % file_written)

            except api.ApplangaConnectionException as e:
                click.secho(str(e), err=True, fg='red')
                return

            except api.ApplangaRequestException as e:
                click.echo('Result: "Error"')
                click.secho('There was a problem with downloading file:\n%s\n' % str(e), err=True, fg='red')
                if str(e).startswith('API response: Error: Tag with name'):
                    click.echo('You might need to push your content in order to have the Tag created first')
                return
