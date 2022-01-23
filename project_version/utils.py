"""
Provide utils for command line interface.
"""
import re


def parse_project_version(version):
    """
    Parse project version to a tuple of integer.

    That can be used for a lexicographical comparison of values.

    Arguments:
        version (str): project version code as a string.

    Returns:
        Parsed project version as a tuple with integer values.
    """
    components = version.split('.')

    return tuple(int(component) for component in components)


def get_non_capitalized_pull_request_title(commit_message: str) -> str:
    """
    Extract non capitalized pull request title from a commit message.

    Arguments:
        commit_message (str): the commit message from where to extract the pull request title.

    Returns:
        The non-capitalized pull request title as string.
    """
    summary = commit_message.splitlines()[0]
    non_capitalized_summary = summary[0].lower() + summary[1:]
    pull_request_reference_pattern = r'\s+\(#\d+\).*'

    return re.sub(
        pattern=pull_request_reference_pattern,
        repl='',
        string=non_capitalized_summary,
    )
