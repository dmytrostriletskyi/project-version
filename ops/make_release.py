"""
Provide implementation of making a release.
"""
import sys
import os

import re

from github import Github


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


if __name__ == '__main__':
    _, target_branch, version = sys.argv

    github_access_token = os.environ.get('GIT_HUB_ACCESS_TOKEN')

    github = Github(login_or_token=github_access_token)
    repository = github.get_repo('dmytrostriletskyi/project-version')

    target_commit = repository.get_commit(sha=target_branch)
    commit_message = target_commit.commit.message

    release_message = f'v{version}: {get_non_capitalized_pull_request_title(commit_message)}'

    repository.create_git_release(
        tag=f'v{version}',
        name=release_message,
        message='\u2800',  # https://www.compart.com/en/unicode/U+2800
        target_commitish=target_branch,
    )
