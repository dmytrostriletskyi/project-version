"""
Provide services for command line interface.
"""
from github import Github

from project_version.utils import parse_project_version


class CheckProjectVersion:
    """
    Check a project version service.
    """

    NOT_CHANGED_REASON = 'Project version file is not changed.'
    MAJOR_VERSION_CANNOT_BE_DECREASED_REASON = 'Major version cannot be decreased.'
    MINOR_VERSION_CANNOT_BE_DECREASED_REASON = 'Minor version cannot be decreased.'
    PATCH_VERSION_CANNOT_BE_DECREASED_REASON = 'Patch version cannot be decreased.'
    MAJOR_VERSION_MORE_THAN_PLUS_ONE_REASON = 'Major version cannot be increased by more than on 1.'
    MINOR_VERSION_MORE_THAN_PLUS_ONE_REASON = 'Minor version cannot be increased by more than on 1.'
    PATCH_VERSION_MORE_THAN_PLUS_ONE_REASON = 'Patch version cannot be increased by more than on 1.'
    PATCH_VERSION_ZEROED_REASON = 'Patch version needs to be zeroed when minor is updated.'
    MAJOR_VERSION_ZEROED_REASON = 'Both patch and minor version needs to be zeroed when major is updated.'

    def __init__(self, organization, repository, base_branch, head_branch, access_token):
        """
        Construct the object.

        Arguments:
            organization (str): a provider's organization name.
            repository (str): a provider's repository name.
            base_branch (str): a branch to compare a project version with. Usually, a default branch.
            head_branch (str): a branch to get its project version for comparison. Usually, a feature branch.
            access_token (str): a provider's API access token.

        Returns:
            True and None, if check project version can be increased.
            Otherwise, False and reason as a string.
        """
        self.organization = organization
        self.repository = repository
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.access_token = access_token

    def call(self):
        """
        Check a project version.
        """
        github = Github(login_or_token=self.access_token)
        repository = github.get_repo(full_name_or_id=f'{self.organization}/{self.repository}')

        base_branch_project_version_file = repository.get_contents('.project-version', ref=self.base_branch)
        base_branch_project_version = base_branch_project_version_file.decoded_content.decode().replace('\n', '')

        head_branch_project_version_file = repository.get_contents('.project-version', ref=self.head_branch)
        head_branch_project_version = head_branch_project_version_file.decoded_content.decode().replace('\n', '')

        if base_branch_project_version == head_branch_project_version:
            return False, CheckProjectVersion.NOT_CHANGED_REASON

        (
            base_branch_major_version,
            base_branch_minor_version,
            base_branch_patch_version
        ) = parse_project_version(base_branch_project_version)

        (
            head_branch_major_version,
            head_branch_minor_version,
            head_branch_patch_version
        ) =  parse_project_version(head_branch_project_version)

        major_difference = int(head_branch_major_version) - int(base_branch_major_version)
        minor_difference = int(head_branch_minor_version) - int(base_branch_minor_version)
        patch_difference = int(head_branch_patch_version) - int(base_branch_patch_version)

        if major_difference < 0:
            return False, CheckProjectVersion.MAJOR_VERSION_CANNOT_BE_DECREASED_REASON

        if not major_difference and minor_difference < 0:
            return False, CheckProjectVersion.MINOR_VERSION_CANNOT_BE_DECREASED_REASON

        if not major_difference and not minor_difference and patch_difference < 0:
            return False, CheckProjectVersion.PATCH_VERSION_CANNOT_BE_DECREASED_REASON

        if major_difference > 1:
            return False, CheckProjectVersion.MAJOR_VERSION_MORE_THAN_PLUS_ONE_REASON

        if not major_difference and minor_difference > 1:
            return False, CheckProjectVersion.MINOR_VERSION_MORE_THAN_PLUS_ONE_REASON

        if not major_difference and not minor_difference and patch_difference > 1:
            return False, CheckProjectVersion.PATCH_VERSION_MORE_THAN_PLUS_ONE_REASON

        if not major_difference and minor_difference == 1 and head_branch_patch_version != 0:
            return False, CheckProjectVersion.PATCH_VERSION_ZEROED_REASON

        if major_difference == 1 and (head_branch_minor_version != 0 or head_branch_patch_version != 0):
            return False, CheckProjectVersion.MAJOR_VERSION_ZEROED_REASON

        return True, None
