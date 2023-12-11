"""cpytest package entry point. used to check for required package versions."""

import sys
from importlib.metadata import version
from packaging.version import parse

from termcolor import colored


def check_min_package_version(package_name: str, min_version: str) -> None:
    try:
        pkg_version = version(package_name)
    except Exception as exc:
        raise RuntimeError(f"Failed to get {package_name} version: {exc}") from exc

    if parse(pkg_version) < parse(min_version):
        text = f"cpytest dependency error: {package_name} >= {min_version} is required (found: {pkg_version}). "
        note = (
            f"Please install it with `pip install {package_name}>={min_version}`\n"
            "Note: Due to a dependency conflict with `pycparserext`, this can't be done automatically.\n"
            "      You can ignore any dependency conflict warnings from pip."
        )
        print(colored(text, "red"), file=sys.stderr)
        print(colored(note, "yellow"), file=sys.stderr)
        sys.exit(1)


check_min_package_version("pycparser", "2.21")
