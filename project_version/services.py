"""
Provide services for command line interface.
"""
from github import Github

from project_version.abstarct import AbstractCheckProjectVersion
from project_version.utils import (
    get_non_capitalized_pull_request_title,
    parse_project_version,
)


class GitHubCheckProjectVersion(AbstractCheckProjectVersion):
    """
    GitHub check a project version service.
    """

    def get_project_versions(self):
        """
        Get project versions for base and head branches.

        Returns:
            Base and head branches project versions as a tuple of strings.
        """
        github = Github(login_or_token=self.access_token)
        repository = github.get_repo(full_name_or_id=f'{self.organization}/{self.repository}')

        base_branch_project_version_file = repository.get_contents('.project-version', ref=self.base_branch)
        base_branch_project_version = base_branch_project_version_file.decoded_content.decode().replace('\n', '')

        head_branch_project_version_file = repository.get_contents('.project-version', ref=self.head_branch)
        head_branch_project_version = head_branch_project_version_file.decoded_content.decode().replace('\n', '')

        return base_branch_project_version, head_branch_project_version


class GitHubBumpProjectVersion:
    """
    GitHub bump a project version service.
    """

    def __init__(self, organization, repository, base_branch, head_branch, access_token):
        """
        Construct the object.

        Arguments:
            organization (str): the provider's organization name.
            repository (str): the provider's repository name.
            base_branch (str): a branch to get a project version from. Usually, a default branch.
            head_branch (str): a branch to push bumped project version to. Usually, a feature branch.
            access_token (str): the provider's API access token.
        """
        self.organization = organization
        self.repository = repository
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.access_token = access_token

    def call(self):
        """
        Bump a project version.

        Returns:
            True and None, if project version's bumping succeed.
            Otherwise, False and reason as a string.
        """
        github = Github(login_or_token=self.access_token)
        repository = github.get_repo(full_name_or_id=f'{self.organization}/{self.repository}')

        base_branch_project_version_file = repository.get_contents('.project-version', ref=self.base_branch)
        base_branch_project_version = base_branch_project_version_file.decoded_content.decode().replace('\n', '')

        (
            base_branch_major_version,
            base_branch_minor_version,
            base_branch_patch_version,
        ) = parse_project_version(base_branch_project_version)

        increased_base_branch_patch_version = int(base_branch_patch_version) + 1

        increased_base_branch_project_version = \
            f'{base_branch_major_version}.{base_branch_minor_version}.{increased_base_branch_patch_version}'

        repository.update_file(
            path='.project-version',
            message=f'Bump project version to {increased_base_branch_project_version}',
            content=f'{increased_base_branch_project_version}\n',
            sha=repository.get_contents('.project-version', ref=self.head_branch).sha,
            branch=self.head_branch,
        )

        return True, None


class GitHubRelease:
    """
    GitHub release service.
    """

    def __init__(self, organization, repository, branch, project_version, access_token):
        """
        Construct the object.

        Arguments:
            organization (str): the provider's organization name.
            repository (str): the provider's repository name.
            branch (str):  branch to make a release for.
            project_version (str): a project version to make a release with.
            access_token (str): the provider's API access token.
        """
        self.organization = organization
        self.repository = repository
        self.branch = branch
        self.project_version = project_version
        self.access_token = access_token

    def call(self):
        """
        Make a release based on a project version.

        Returns:
            True and None, if release succeed.
            Otherwise, False and reason as a string.
        """
        github = Github(login_or_token=self.access_token)
        repository = github.get_repo(full_name_or_id=f'{self.organization}/{self.repository}')

        target_commit = repository.get_commit(sha=self.branch)
        commit_message = target_commit.commit.message

        release_message = f'v{self.project_version}: {get_non_capitalized_pull_request_title(commit_message)}'

        repository.create_git_release(
            tag=f'v{self.project_version}',
            name=release_message,
            message='\u2800',  # https://www.compart.com/en/unicode/U+2800
            target_commitish=self.branch,
        )

        return True, None
