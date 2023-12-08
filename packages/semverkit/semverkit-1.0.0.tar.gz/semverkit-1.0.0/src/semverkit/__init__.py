from typing import Optional, Union

import click
from semver import Version

ERROR_FMT = "[error] {}"
PART_LABELS = [
    "1",
    "major",
    "2",
    "minor",
    "3",
    "patch",
    "4",
    "prerelease",
    "5",
    "build",
]


def create_invalid_part_error(part: str, /) -> ValueError:
    return ValueError(f"part '{part}' is invalid")


def exit_with_error(error: str, exit_code: int = 2, fmt: str = ERROR_FMT) -> None:
    click.echo(fmt.format(error), err=True)
    exit(exit_code)


def unpack_optional_str(s: Optional[str]) -> str:
    return "" if s is None else s


def bump(part: str, version: Version, /) -> Version:
    part = part.casefold()
    if part in ("1", "major"):
        return version.bump_major()
    elif part in ("2", "minor"):
        return version.bump_minor()
    elif part in ("3", "patch"):
        return version.bump_patch()
    elif part in ("4", "prerelease"):
        return version.bump_prerelease()
    elif part in ("5", "build"):
        return version.bump_build()
    else:
        raise create_invalid_part_error(part)


def extract(part: str, version: Version, /) -> Union[int, str]:
    part = part.casefold()
    if part in ("1", "major"):
        return version.major
    elif part in ("2", "minor"):
        return version.minor
    elif part in ("3", "patch"):
        return version.patch
    elif part in ("4", "prerelease"):
        return unpack_optional_str(version.prerelease)
    elif part in ("5", "build"):
        return unpack_optional_str(version.build)
    else:
        raise create_invalid_part_error(part)


@click.group()
def run() -> None:
    pass


@run.command(name="bump")
@click.argument("part", type=click.Choice(choices=PART_LABELS, case_sensitive=False))
@click.argument("version", type=Version.parse)
def bump_command(part: str, version: Version) -> None:
    """Bumps a PART of VERSION."""
    result = bump(part, version)
    click.echo(result)


@run.command(name="compare")
@click.argument("version", type=Version.parse)
@click.argument("other", type=Version.parse)
def compare_command(version: Version, other: Version) -> None:
    """Compares VERSION against OTHER.

    Returns '0' if VERSION is equal to OTHER.

    Returns '-1' if VERSION is less than OTHER.

    Returns '1' if VERSION is greater than OTHER.
    """
    result = version.compare(other)
    click.echo(result)


@run.command(name="extract")
@click.argument("part", type=click.Choice(choices=PART_LABELS, case_sensitive=False))
@click.argument("version", type=Version.parse)
def extract_command(part: str, version: Version) -> None:
    """Extracts a PART of VERSION.

    Usage: semverkit extract prerelease 1.2.3-rc.5

           rc.5
    """
    result = extract(part, version)
    click.echo(result)


@run.command(name="finalize")
@click.argument("version", type=Version.parse)
def finalize_command(version: Version) -> None:
    """Removes any prerelease and build metadata from VERSION.

    Usage: semverkit finalize 1.2.3-rc.5

           1.2.3
    """
    result = version.finalize_version()
    click.echo(result)


@run.command(name="iscompatible")
@click.argument("version", type=Version.parse)
@click.argument("other", type=Version.parse)
def is_compatible_command(version: Version, other: Version) -> None:
    """Exits with 1 if VERSION is not compatible with OTHER."""
    if not version.is_compatible(other):
        exit_with_error(f"'{version}' is not compatible with '{other}'")


@run.command(name="ismatch")
@click.argument("expression", type=str)
@click.argument("version", type=Version.parse)
def is_match_command(expression: str, version: Version) -> None:
    """Exits with 1 if VERSION does not match EXPRESSION.

    Usage: semverkit ismatch '>=1.0.0' 2.0.0
    """
    if not version.match(expression):
        exit_with_error(f"'{version}' does not match expression '{expression}'")


@run.command(name="isvalid")
@click.argument("version", type=str)
def is_valid_command(version: str) -> None:
    """Exits with 1 if VERSION is invalid."""
    if not Version.is_valid(version):
        exit_with_error(f"'{version}' is invalid")


@run.command(name="replace")
@click.argument("version", type=Version.parse)
@click.option("-1", "--major", type=int)
@click.option("-2", "--minor", type=int)
@click.option("-3", "--patch", type=int)
@click.option("-4", "--prerelease", type=str)
@click.option("-5", "--build", type=str)
def replace_command(
    version: Version,
    major: Optional[int] = None,
    minor: Optional[int] = None,
    patch: Optional[int] = None,
    prerelease: Optional[str] = None,
    build: Optional[str] = None,
) -> None:
    """Replaces one or more parts of VERSION.

    Usage: semverkit replace 1.2.3-alpha.4 --prerelease rc.1

           1.2.3-rc.1
    """
    replace_kwargs = {}
    if major is not None:
        replace_kwargs["major"] = major
    if minor is not None:
        replace_kwargs["minor"] = minor
    if patch is not None:
        replace_kwargs["patch"] = patch
    if prerelease is not None:
        replace_kwargs["prerelease"] = prerelease
    if build is not None:
        replace_kwargs["build"] = build
    result = version.replace(**replace_kwargs)
    click.echo(result)


@run.command(name="split")
@click.argument("version", type=Version.parse)
@click.option("--delimiter", type=str, default="\0")
def split_command(version: Version, delimiter: str) -> None:
    """Splits parts of VERSION."""
    parts = [
        str(version.major),
        str(version.minor),
        str(version.patch),
        unpack_optional_str(version.prerelease),
        unpack_optional_str(version.build),
    ]
    if delimiter != "\0":
        click.echo(delimiter.join(parts))
    else:
        for part in parts:
            click.echo(part)


__name__ = "semverkit"
__version__ = "1.0.0"
__all__ = [
    "bump",
    "extract",
    "run",
]
