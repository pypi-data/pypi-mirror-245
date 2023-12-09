# semverkit

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/semverkit?logo=python&logoColor=yellow)](https://github.com/elmernocon/semverkit)
[![PyPI - Version](https://img.shields.io/pypi/v/semverkit?logo=pypi&logoColor=yellow)](https://pypi.org/project/semverkit/)
[![Static Badge](https://img.shields.io/badge/executable-latest-blue?logo=github)](https://github.com/elmernocon/semverkit/releases/latest/download/semverkite)
[![GitHub License](https://img.shields.io/github/license/elmernocon/semverkit?logo=github)](https://raw.githubusercontent.com/elmernocon/semverkit/main/LICENSE)
[![Docker Image Size (tag)](https://img.shields.io/docker/image-size/elmernocon/semverkit/latest?logo=docker&label=size)](https://hub.docker.com/repository/docker/elmernocon/semverkit)

A thin CLI wrapper for the Python package [semver](https://python-semver.readthedocs.io/).

## Installation and Usage

PyPI

```shell
$ pip install semverkit
```

```shell
$ python -m semverkit
```

or

```shell
$ semverkit
```

---

Docker

```shell
$ docker run --rm elmernocon/semverkit
```

---

Curl

```shell
$ curl -Ls https://github.com/elmernocon/semverkit/releases/latest/download/semverkite -o semverkit && chmod +x semverkit
```

```shell
$ semverkit
```

---

```text
Usage: semverkit [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bump          Bumps a PART of VERSION.
  compare       Compares VERSION against OTHER.
  extract       Extracts a PART of VERSION.
  finalize      Removes any prerelease and build metadata from VERSION.
  iscompatible  Exits with 1 if VERSION is not compatible with OTHER.
  ismatch       Exits with 1 if VERSION does not match EXPRESSION.
  isvalid       Exits with 1 if VERSION is invalid.
  replace       Replaces one or more parts of VERSION.
  split         Splits parts of VERSION.
```
