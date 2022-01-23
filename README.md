Explicit, strict and automatic project version management based on semantic versioning.

[![](https://github.com/dmytrostriletskyi/project-version/actions/workflows/trunk.yml/badge.svg?branch=master)](https://github.com/dmytrostriletskyi/project-version/actions/workflows/trunk.yml)
[![](https://img.shields.io/github/release/dmytrostriletskyi/project-version.svg)](https://github.com/dmytrostriletskyi/project-version/releases)
[![](https://img.shields.io/pypi/v/project-version.svg)](https://pypi.python.org/pypi/project-version)

[![](https://pepy.tech/badge/project-version)](https://pepy.tech/project/project-version)
[![](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/pypi/pyversions/project-version.svg)](https://pypi.python.org/pypi/project-version/)

* [Getting started](#getting-started)
  * [End users](#end-users)
  * [Semantic versioning](#semantic-versioning)
  * [Project version](#project-version)
  * [Motivation](#motivation)
* [Command line interface](#command-line-interface)
  * [Installation](#installation)
  * [Version](#version)
  * [Help](#help)
  * [Check](#check)
  * [Bump](#bump)
  * [Release](#release)
  * [Examples](#examples)
* [FAQ](#faq)
* [Contributing](#contributing)

## Getting started

If you found this project useful, but it does not really fit your development and releasing processes, 
[create an issue](https://github.com/dmytrostriletskyi/project-version/issues) with your proposals, please.

Also, if you have any questions after reading the documentation, check [FAQ](#faq). If there are no answers,
[create an issue](https://github.com/dmytrostriletskyi/project-version/issues) with your question, please.

### End users

An end user of the project is a software engineer or DevOps guy who develop projects that needs explicit, strict and 
automatic project version management for tags, images, API and/or libraries.

### Semantic versioning

There is the [semantic versioning](https://semver.org/). To make a long story short, it is versioning specification
with major, minor and patch numbers telling us what the current version of a project is and how to react on its new 
versions' updates. Example of the project version following semantic versioning is `1.3.12` where the first digit is
major number, the second digit is minor number, and the third digit is patch number.

These are the rules of increasing chose numbers:

1. Increase major version when you make incompatible API changes such as change a name of a required function's or API
   parameter.
   
   ```bash
   Before changes: 1.3.12
   After changes: 2.0.0
   ```

2. Increase minor version when you add functionality in a backwards compatible manner such as add a new optional
   function's or API parameter.
   
   ```bash
   Before changes: 1.3.12
   After changes: 1.4.0
   ```

3. Increase match version when you make backwards compatible bug fixes.

   ```bash
   Before changes: 1.3.12
   After changes: 1.3.13
   ```

You have probably seen semantic versioning in your programming language's packages such as 
[JavaScript's axios](https://www.npmjs.com/package/axios) (e.g. version `0.24.0`) or 
[Python requests](https://pypi.org/project/requests/) (e.g. version `2.27.1`).

### Project version

`project version` is just a set of principles to maintain project versioning and 
[command line interface](#command-line-interface) that helps not to forget about those principles such as a code style 
and linters to check its compliance. 

`project version` requires having a file named `.project-version` in the root directory containing a project version. 
With this file, developers declare single source to fetch a project version from for things like `Git` tags or `Docker` 
images. 

![](/assets/project-version-file.png)

### Usage

Now you can reuse a project version from `.project-version` file for multiple release-related purposes:

1. There may be situations when you deployed the new version of an application but do not have deployment logs, or you 
   deployed the new version of a application but logs tell nothing, or do not have `Git` information. In all the cases 
   it may be useful to enter your application's runtime and check file `.project-version` to know the exact version 
   which is related to the codebase. 
   
   ```bash
   $ cat .project-version
   1.3.12
   ```

2. Instead of using `Git` commit SHA or its short version for `Docker` images, you can use a project version.
   
   ```bash
   $ docker build --tag facebook/react:v$(cat .project-version) -f Dockerfile .
   ```

3. Instead of using `Git` commit SHA or its short version for `GitHub` release version number, you can use a project 
   version.
   
   ```yaml
   on:
     push:
       branches:
         - master
     
      jobs:
       release:
         runs-on: [ubuntu-latest]
         steps:
           - uses: actions/checkout@v2
           - name: Create Release
             uses: actions/create-release@v1
             with:
               tag_name: $(cat .project-version)
               release_name: Release v$(cat .project-version)
   ```

4. Instead of supporting package version (`Python package`, `Gem` or `JAR`) in a dedicated file, you can automatically 
   use a project version. `Python package` with its `setup.py` for building packages is illustrated below:
  
   ```python
   with open('.project-version', 'r') as project_version_file:
       project_version = project_version_file.read().strip()
  
   setup(
       version=project_version,
       name='project-version',
       ...
   )
   ```

5. In case you manage an infrastructure as a code (e.g. `Kubernetes`), you may face challenges of supporting multiple
   major version of your project (e.g. `HTTP API`). Without automation, you should create new major version 
   configurations manually.

   Let us consider the example where you have API's first version deployment configurations:
    
   ```bash
   $ ls deployment/
   ├── deployment
   │   ├── v1
   │   │   └── deployment.yaml
   │   │   └── ingress.yaml
   │   │   └── service.yaml
   
   $ cat /deployment/v1/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     namespace: api-v1
   ```
   
   When it is time to create API's second version, you can simply copy previous version configurations and substitute
   `v1` to `v2`.

   ```bash
   $ echo .project-version
   2.0.0
   $ export PROJECT_PREVIOUS_MAJOR_VERSION=$(($cat .project-version)-1); echo $PROJECT_MAJOR_VERSION
   1
   $ export PROJECT_MAJOR_VERSION=$(cut -d '.' -f 1 <<< "$(cat .project-version)"); echo $PROJECT_PREVIOUS_MAJOR_VERSION
   2
   $ cp -r deployment/v$PROJECT_PREVIOUS_MAJOR_VERSION deployment/v$PROJECT_MAJOR_VERSION
   $ find deployment/ -type f -exec sed -i \
         's/namespace: v$PROJECT_PREVIOUS_MAJOR_VERSION/namespace: v$PROJECT_MAJOR_VERSION/g' {} +
   ```

   After, you automatically get deployment configurations for the new version:

   ```yaml
   $ ls deployment/
   ├── deployment
   │   ├── v1
   │   │   └── deployment.yaml
   │   │   └── ingress.yaml
   │   │   └── service.yaml
   │   ├── v2
   │   │   └── deployment.yaml
   │   │   └── ingress.yaml
   │   │   └── service.yaml
   
   $ cat /deployment/v2/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     namespace: api-v2
   ```
   
And there is much more cases when relying on a project version from its file makes software releasing easier.

### Maintenance

All use cases described above requires a project version always be up-to-date and never corrupted. In case it is not,
you can release the same version twice, for example. To avoid this, `project-version` is tightly bound to a branching
model with its release life-cycle. Let's consider how `project-version` works with the most popular branching models
`Git flow` and `GitHub flow`.

In `Git flow`, developers do features in feature branches and merge them to `develop` branch. When `develop` branch
has a set of features merged, a release is created (with a separate branch for it) and deployed. To define a release 
version, `project-version` requests a developer to make an additional commit into `develop` branch that changes 
`.project-version` file.

<img src="/assets/git-flow.png" width="600" height="401">

In `GitHub flow`, developers do features in feature branches and merge them to `develop` branch. Once a single feature
is merged to `develop` branch, a release is immediately created (with no separate branch) and deployed. To define a
release version, `project-version` requests a developer to make an additional commit into a feature branch that changes 
`.project-version` file.

<img src="/assets/git-hub-flow.png" width="600" height="316">

## Command line interface

This chapter describes a set of command line interface (automation scripts) with descriptive explanation of its 
use-cases that help to manage a project version. The command line interface is completely optional but helpful. It
helps developers not to forget about increasing a project version or auto-increase when needed.

### Installation

Install using `pip3`:

```bash
$ pip3 install project-version
```

### Version

Get the version of the package — `project-version --version`:

```bash
$ project-version --version
project-version, version 0.1.0
```

### Help

Get the detailed description of all supported commands by the package — `project-version --help`:

```bash
$ project-version --help
Usage: project-version [OPTIONS] COMMAND [ARGS]...

  Project version command-line interface.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  check  Check whether specified project version is increased properly.
```

### Check

Check whether specified project version is increased properly — `project-version check`.

Parameters:

| Argument     | Type   | Required | Restrictions      | Description                                                                                                                                         |
|:-------------|:------:|:--------:|:-----------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| provider     | String | Yes      | One of: `GitHub`. | A provider of hosting for software development and version control name.                                                                            |
| organization | String | Yes      | -                 | The provider's organization name.                                                                                                                   |
| repository   | String | Yes      | -                 | The provider's repository name.                                                                                                                     |
| base-branch  | String | Yes      | -                 | A branch to compare a project version with. Usually, a default branch.                                                                              |
| head-branch  | String | Yes      | -                 | A branch to get its project version for comparison. Usually, a feature branch.                                                                      |
| access-token | String | Yes      | -                 | The provider's [API access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). |

Example of usage:

```bash
$ project-version check \
    --provider=GitHub \
    --organization=facebook \
    --repository=react \
    --base-branch=master \
    --head-branch=map-children-components \ 
    --access-token=ghp_0TI5LBBLNyKlT5Lv8eR6EIOB0hkopMqz5LWjNyKlZ1
```

Example of workflow:

```yaml
---
name: Pull request workflow

on:
  pull_request_target:
    branches:
      - master

jobs:
  check-project-version:
    runs-on: [ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Install project version
        run: pip3 install project-version
      - name: Check a project version
        run: |
          project-version check \
              --provider=GitHub \
              --organization=facebook \
              --repository=react \
              --base-branch=master \
              --head-branch=map-children-components \ 
              --access-token=${{ secrets.GIT_HUB_ACCESS_TOKEN }}
```

### Bump

Bump the minor version of a project version — `project-version bump`.

Parameters:

| Argument     | Type   | Required | Restrictions      | Description                                                                                                                                         |
|:-------------|:------:|:--------:|:-----------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| provider     | String | Yes      | One of: `GitHub`. | A provider of hosting for software development and version control name.                                                                            |
| organization | String | Yes      | -                 | The provider's organization name.                                                                                                                   |
| repository   | String | Yes      | -                 | The provider's repository name.                                                                                                                     |
| base-branch  | String | Yes      | -                 | A branch to get a project version from. Usually, a default branch.                                                                              |
| head-branch  | String | Yes      | -                 | A branch to push bumped project version to. Usually, a feature branch.                                                                      |
| access-token | String | Yes      | -                 | The provider's [API access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). |

Example of usage:

```bash
$ project-version bump \
    --provider=GitHub \
    --organization=facebook \
    --repository=react \
    --base-branch=master \
    --head-branch=dependabot/npm/core-js-3.6.4 \ 
    --access-token=ghp_0TI5LBBLNyKlT5Lv8eR6EIOB0hkopMqz5LWjNyKlZ1
```

Example of workflow:

```yaml
---
name: Pull request workflow

on:
  pull_request_target:
    branches:
      - master

jobs:
  check-project-version:
    runs-on: [ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Install project version
        run: pip3 install project-version
      - name: Bump project version if it is non-human pull request
        if: ${{ github.actor == 'dependabot[bot]' || github.actor == 'facebook-bot' }}
        run: |
          project-version bump \
              --provider=GitHub \
              --organization=facebook \
              --repository=react \
              --base-branch=master \
              --head-branch=map-children-components \ 
              --access-token=${{ secrets.GIT_HUB_ACCESS_TOKEN }}
```

### Release

Make a release — `project-version release`.

Parameters:

| Argument        | Type   | Required | Restrictions      | Description                                                                                                                                         |
|:----------------|:------:|:--------:|:-----------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| provider        | String | Yes      | One of: `GitHub`. | A provider of hosting for software development and version control name.                                                                            |
| organization    | String | Yes      | -                 | The provider's organization name.                                                                                                                   |
| repository      | String | Yes      | -                 | The provider's repository name.                                                                                                                     |
| branch          | String | Yes      | -                 | A branch to make a release for                                                                                                                      |
| project-version | String | Yes      | -                 | A project version to make a release with.                                                                                                           |
| access-token    | String | Yes      | -                 | The provider's [API access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). |

Example of usage:

```bash
$ project-version release \
    --provider=GitHub \
    --organization=dmytrostriletskyi \
    --repository=project-version \
    --branch=master \
    --project-version=1.1.3 \
    --access-token=ghp_0TI5LBBLNyKlT5Lv8eR6EIOB0hkopMqz5LWjNyKlZ1
```

Example of workflow:

```yaml
---
name: Master workflow

on:
  push:
    branches:
      - master

jobs:
  release:
    runs-on: [ubuntu-latest]
    outputs:
      project_version: ${{ steps.get_project_version.outputs.project_version }}
    steps:
      - uses: actions/checkout@v2
      - name: Install project version
        run: pip3 install project-version
      - name: Get a version of the project
        id: get_project_version
        run: echo "::set-output name=project_version::$(cat .project-version)"
      - name: Release
        run: |
          project-version release \
              --provider=GitHub \
              --organization=facebook \
              --repository=react \
              --branch=master \
              --project-version=${{ steps.get_project_version.outputs.project_version }} \
              --access-token=${{ secrets.GIT_HUB_ACCESS_TOKEN }}
```

## FAQ

1. **Q:** `project-version`is written in `Python`, but my project's stack is different. Why should I support Python` for 
   this?
  
   **A:** When you develop a project, you do not need `Python`, but only `.project-version` file. The only place you need
   `Python` on is your pipelines runner such as `GitHub Actions`, `Jenkins` or `GitLab CI/CD` to run the command line
   interface. You can use isolated environment such as `Docker` containers:

   ```yaml
   jobs:
     check-project-version:
       runs-on: [ubuntu-latest]
       container:
         image: python:3.9.0-slim
       ...
   ```

2. **Q:** Why should a developer increase a project version manually for a feature, or a set of features?

   **A:** When a developer does a change, the only they know a degree of change: either patch, minor or major. There is
   no machine learning model or other software that can describe a degree of change instead of a person who made those
   changes.
   
3. **Q:** If we merge feature branches often, many concurrent feature branches should pull new project version often. Is
   it fine?

   **A:** Yes, it is fine. It is a price you pay for the project management. Also, keep in mind that most time you
    develop a feature, and only little time you pull other feature branches' changes and merge.

## Contributing

Clone the project and install requirements:

```bash
$ git clone git@github.com:dmytrostriletskyi/accessify.git && cd accessify
$ make install-requirements
```

After changes, ensure the code quality remains the same:

```bash
$ make check-requirements-safety
$ make check-code-complexity
$ make check-code-quality
$ make check-yaml-standards
```

If you are new for the contribution, please read:

* About pull requests — https://help.github.com/en/articles/about-pull-requests
* Create a pull request — https://help.github.com/en/articles/creating-a-pull-request-from-a-fork
* The beginners guide to contributing — https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/
