"""
Provide implementation of command line interface commands.
"""
import sys

import click

from project_version.constants import (
    FAILED_EXIT_CODE,
    SUCCESSFUL_EXIT_CODE,
    GIT_HUB_PROVIDER,
    SUPPORTED_PROVIDERS,
)
from project_version.services import GitHubCheckProjectVersion
from project_version.help import (
    ACCESS_TOKEN,
    ORGANIZATION_NAME_HELP,
    PROVIDER_NAME_HELP,
    REPOSITORY_NAME_HELP,
    BASE_BRANCH,
    HEAD_BRANCH,
)


@click.option('--provider', required=True, type=click.Choice(SUPPORTED_PROVIDERS), help=PROVIDER_NAME_HELP)
@click.option('--organization', required=True, type=str, help=ORGANIZATION_NAME_HELP)
@click.option('--repository', required=True, type=str, help=REPOSITORY_NAME_HELP)
@click.option('--base-branch', required=True, type=str, help=BASE_BRANCH)
@click.option('--head-branch', required=True, type=str, help=HEAD_BRANCH)
@click.option('--access-token', required=True, type=str, help=ACCESS_TOKEN)
@click.command('check')
def check(provider, organization, repository, base_branch, head_branch, access_token) -> None:
    """
    Check whether specified project version is increased properly.
    \f (https://click.palletsprojects.com/en/8.0.x/documentation/#truncating-help-texts)

    Arguments:
        provider (str): A provider of hosting for software development and version control name.
        organization (str): the provider's organization name.
        repository (str): the provider's repository name.
        base_branch (str): a branch to compare a project version with. Usually, a default branch.
        head_branch (str): a branch to get its project version for comparison. Usually, a feature branch.
        access_token (str): a provider's API access token.

    Returns:
        None.
    """
    if provider == GIT_HUB_PROVIDER:
        is_succeed, reason = GitHubCheckProjectVersion(
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
