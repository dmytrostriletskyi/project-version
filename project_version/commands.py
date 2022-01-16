"""
Provide implementation of command line interface commands.
"""
import sys

import click

from project_version.constants import (
    FAILED_EXIT_CODE,
    SUCCESSFUL_EXIT_CODE,
)
from project_version.services import CheckProjectVersion
from project_version.help import (
    ACCESS_TOKEN,
    ORGANIZATION_NAME_HELP,
    REPOSITORY_NAME_HELP,
    BASE_BRANCH,
    HEAD_BRANCH,
)


@click.option('--organization', required=True, type=str, help=ORGANIZATION_NAME_HELP)
@click.option('--repository', required=True, type=str, help=REPOSITORY_NAME_HELP)
@click.option('--base-branch', required=True, type=str, help=BASE_BRANCH)
@click.option('--head-branch', required=True, type=str, help=HEAD_BRANCH)
@click.option('--access-token', required=True, type=str, help=ACCESS_TOKEN)
@click.command('check')
def check(organization, repository, base_branch, head_branch, access_token) -> None:
    """
    Check whether specified project version is increased properly.
    \f (https://click.palletsprojects.com/en/8.0.x/documentation/#truncating-help-texts)

    Arguments:
        organization (str): a provider's organization name.
        repository (str): a provider's repository name.
        base_branch (str): a branch to compare a project version with. Usually, a default branch.
        head_branch (str): a branch to get its project version for comparison. Usually, a feature branch.
        access_token (str): a provider's API access token.

    Returns:
        None.
    """
    is_succeed, reason = CheckProjectVersion(
        organization=organization,
        repository=repository,
        base_branch=base_branch,
        head_branch=head_branch,
        access_token=access_token,
    ).call()

    if not is_succeed:
        click.echo(reason)
        sys.exit(FAILED_EXIT_CODE)

    sys.exit(SUCCESSFUL_EXIT_CODE)
