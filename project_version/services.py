"""
Provide services for command line interface.
"""
from github import Github

from project_version.abstarct import AbstractCheckProjectVersion


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
