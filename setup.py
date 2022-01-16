"""
Setup the package.
"""
from pathlib import Path
from typing import List

from setuptools import (
    find_packages,
    setup,
)

DESCRIPTION = 'Explicitly and strictly control project version with semantic versioning.'
URL = 'https://github.com/dmytrostriletskyi/project-version'

def read_requirements(name: str) -> List[str]:
    """
    Read requirements from a given file in the `requirements` directory.

    Arguments:
        name (str): name of the requirements.

    Returns:
        Requirements in the file as a list of strings.
    """
    requirements_file_path = (Path('requirements') / name).with_suffix('.txt')

    with requirements_file_path.open('r') as requirements_file:
        return requirements_file.read().splitlines()

with open('README.md', 'r') as read_me:
    long_description = read_me.read()


with open('.project-version', 'r') as project_version_file:
    project_version = project_version_file.read().strip()

setup(
    version=project_version,
    name='project-version',
    author='Dmytro Striletskyi',
    author_email='dmytro.striletskyi@gmail.com',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements('project'),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'project-version = project_version.entrypoint:cli',
        ],
    },
)
