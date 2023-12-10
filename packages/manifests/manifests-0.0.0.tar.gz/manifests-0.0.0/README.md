
# manifests [![Package version](https://img.shields.io/pypi/v/manifests?label=PyPI)](https://pypi.org/project/manifests/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/manifests.svg?logo=python&label=Python)](https://pypi.org/project/manifests/)
[![Tests](https://github.com/bswck/manifests/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/manifests/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/manifests.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/manifests)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/manifests.svg?label=License)](https://github.com/bswck/manifests/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Generate code from TOML manifests.

# Installation
If you want to…



## …use this tool in your project 💻
You might simply install it with pip:

```shell
pip install manifests
```

If you use [Poetry](https://python-poetry.org/), then run:

```shell
poetry add manifests
```

## …contribute to [manifests](https://github.com/bswck/manifests) 🚀

<!--
This section was generated from bswck/skeleton@ea3be8a.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/ea3be8a/fragments/guide.md
-->

> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).



1.  Fork the [manifests repository](https://github.com/bswck/manifests) on GitHub.

1.  [Install Poetry](https://python-poetry.org/docs/#installation).<br/>
    Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.
    You might use [pipx](https://github.com/pypa/pipx#readme) to install it globally (recommended):

    ```shell
    pipx install poetry
    ```

    <sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

    Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    ```shell
    pyenv install 3.8
    ```

1.  Clone your fork locally and install dependencies.

    ```shell
    git clone https://github.com/your-username/manifests path/to/manifests
    cd path/to/manifests
    poetry env use $(cat .python-version)
    poetry install
    ```

    Next up, simply activate the virtual environment and install pre-commit hooks:

    ```shell
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/manifests/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [MIT License](https://github.com/bswck/manifests/blob/HEAD/LICENSE).
