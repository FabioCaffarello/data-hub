# Getting Started

There are 2 ways to develop in this workspace:

## Local machine

Install the following softwares

- [node.js 16.x](https://nodejs.org/en/download/)
- [golang](https://golang.google.cn/)
- [docker](https://www.docker.com/)
- [docker-compose](https://www.docker.com/)
- [Terraform](https://www.terraform.io/)
- [poetry](https://pypi.org/project/poetry/1.2.0b2/)


```shell
pip install poetry==1.2.0b3
```

> Installation using [pipx](https://pypa.github.io/pipx/installation/) is strongly recommended.


## Using Docker Dev Container

### Using Visual Studio Code Development Container

To use the VSCode [devcontainer](https://code.visualstudio.com/docs/remote/containers) feature, the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension needs to be installed.

With this extension installed, when you open the folder in the VSCode a pop-up shows up asking to reopen the window using the devcontainer.

> The Docker service needs to be running.

### Git Credentials

[Visual Studio - Remote Container - Sharing Git Credentials](https://code.visualstudio.com/docs/remote/containers#_sharing-git-credentials-with-your-container)


## Install dependencies

```shell
npm install
```

```shell
poetry install
```

## Terminal virtual environment

```shell
poetry shell
```

## Run Unit Tests

```shell
npx nx affected:test
```

or for a specific project

```shell
npx nx <appName>:test
```

## Run Flake8 Linting

```shell
npx nx affected:lint
```

or for a specific project

```shell
npx nx lint <appName>
```

## Add new dependency

```shell
npx nx run <appName>:add --name <dependencyName>==<dependencyVersion>
```

Example:

```shell
npx nx run thinkific-webhook:add --name requests=2.27.1
```

Using the Nx wrapper to adding a dependency ensure that both root `poetry.lock` and project `poetry.lock` are updated.

## Generate new Python Library

```shell
npx nx generate @data-hub/python-tools:create-project <LibName> --description=<LibDescription> --packageName=<LibPackageName> --moduleName=<LibModuleName> --directory=<LibDir> --type=library
```

Example:

```shell
npx nx generate @data-hub/python-tools:create-project base-parser --description='base parser.' --packageName=base-parser --type=library --directory=ingestors --moduleName=baseparser
```
