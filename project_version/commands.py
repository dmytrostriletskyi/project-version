"""
Provide implementation of command line interface commands.
"""
import sys

import click

from project_version.constants import (
    FAILED_EXIT_CODE,
    GIT_HUB_PROVIDER,
    SUCCESSFUL_EXIT_CODE,
    SUPPORTED_PROVIDERS,
)
from project_version.help import (
    ACCESS_TOKEN,
    BASE_BRANCH,
    BRANCH,
    HEAD_BRANCH,
    ORGANIZATION_NAME_HELP,
    PROJECT_VERSION,
    PROVIDER_NAME_HELP,
    REPOSITORY_NAME_HELP,
)
from project_version.services import (
    GitHubBumpProjectVersion,
    GitHubCheckProjectVersion,
    GitHubRelease,
)


@click.option('--provider', required=True, type=click.Choice(SUPPORTED_PROVIDERS), help=PROVIDER_NAME_HELP)
@click.option('--organization', required=True, type=str, help=ORGANIZATION_NAME_HELP)
@click.option('--repository', required=True, type=str, help=REPOSITORY_NAME_HELP)
@click.option('--base-branch', required=True, type=str, help=BASE_BRANCH)
@click.option('--head-branch', required=True, type=str, help=HEAD_BRANCH)
@click.option('--access-token', required=True, type=str, help=ACCESS_TOKEN)
@click.command('check')
def check(provider, organization, repository, base_branch, head_branch, access_token) -> None:
    r"""
    Check whether specified project version is increased properly.
    \f (https://click.palletsprojects.com/en/8.0.x/documentation/#truncating-help-texts)

    Arguments:
        provider (str): A provider of hosting for software development and version control name.
        organization (str): the provider's organization name.
        repository (str): the provider's repository name.
        base_branch (str): a branch to compare a project version with. Usually, a default branch.
        head_branch (str): a branch to get its project version for comparison. Usually, a feature branch.
        access_token (str): a provider's API access token.
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


@click.option('--provider', required=True, type=click.Choice(SUPPORTED_PROVIDERS), help=PROVIDER_NAME_HELP)
@click.option('--organization', required=True, type=str, help=ORGANIZATION_NAME_HELP)
@click.option('--repository', required=True, type=str, help=REPOSITORY_NAME_HELP)
@click.option('--base-branch', required=True, type=str, help=BASE_BRANCH)
@click.option('--head-branch', required=True, type=str, help=HEAD_BRANCH)
@click.option('--access-token', required=True, type=str, help=ACCESS_TOKEN)
@click.command('bump')
def bump(provider, organization, repository, base_branch, head_branch, access_token) -> None:
    r"""
    Bump the minor version of a project version.
    \f (https://click.palletsprojects.com/en/8.0.x/documentation/#truncating-help-texts)

    Arguments:
        provider (str): A provider of hosting for software development and version control name.
        organization (str): the provider's organization name.
        repository (str): the provider's repository name.
        base_branch (str): a branch to get a project version from. Usually, a default branch.
        head_branch (str): a branch to push bumped project version to. Usually, a feature branch.
        access_token (str): a provider's API access token.
    """
    if provider == GIT_HUB_PROVIDER:
        is_succeed, reason = GitHubBumpProjectVersion(
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


@click.option('--provider', required=True, type=click.Choice(SUPPORTED_PROVIDERS), help=PROVIDER_NAME_HELP)
@click.option('--organization', required=True, type=str, help=ORGANIZATION_NAME_HELP)
@click.option('--repository', required=True, type=str, help=REPOSITORY_NAME_HELP)
@click.option('--branch', required=True, type=str, help=BRANCH)
@click.option('--project-version', required=True, type=str, help=PROJECT_VERSION)
@click.option('--access-token', required=True, type=str, help=ACCESS_TOKEN)
@click.command('release')
def release(provider, organization, repository, branch, project_version, access_token) -> None:
    r"""
    Make a release based on a project version.
    \f (https://click.palletsprojects.com/en/8.0.x/documentation/#truncating-help-texts)

    Arguments:
        provider (str): A provider of hosting for software development and version control name.
        organization (str): the provider's organization name.
        repository (str): the provider's repository name.
        branch (str): a branch to make a release for.
        project_version (str): a project version to make a release with.
        access_token (str): a provider's API access token.
    """
    if provider == GIT_HUB_PROVIDER:
        is_succeed, reason = GitHubRelease(
            organization=organization,
            repository=repository,
            branch=branch,
            project_version=project_version,
            access_token=access_token,
        ).call()

    if not is_succeed:
        click.echo(reason)
        sys.exit(FAILED_EXIT_CODE)

    sys.exit(SUCCESSFUL_EXIT_CODE)
