r"""
Functions related to the command-line interface (CLI) for the nubs library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to the nubs library by David C. Stauffer in July 2026.

"""

# %% Imports
import doctest
from enum import Enum
from functools import lru_cache
from pathlib import Path
import sys
import unittest

from nubs.version import version_info


# %% Enums - _ReturnCodes
class _ReturnCodes(int, Enum):
    r"""
    Return codes for use as outputs in the command line API.

    Examples
    --------
    >>> from nubs.cli import _ReturnCodes
    >>> rc = _ReturnCodes.clean
    >>> print(rc)
    _ReturnCodes.clean: 0

    """

    # fmt: off
    clean            = 0  # Clean exit
    bad_command      = 1  # Unexpected command
    bad_folder       = 2  # Folder to execute a command in doesn't exist
    bad_help_file    = 3  # help file doesn't exist
    bad_version      = 4  # version information cannot be determined
    test_failures    = 5  # A test ran to completion, but failed its criteria
    no_coverage_tool = 6  # Coverage tool is not installed
    # fmt: on

    def __str__(self) -> str:
        r"""Return string representation."""
        return f"{self.__class__.__name__}.{self.name}: {self.value}"


# %% Functions - get_root_dir
@lru_cache
def get_root_dir() -> Path:
    r"""
    Return the folder that contains this source file and thus the root folder for the whole code.

    Returns
    -------
    class pathlib.Path
        Location of the folder that contains all the source files for the code.

    Notes
    -----
    #.  Written by David C. Stauffer in July 2026.

    Examples
    --------
    >>> from nubs import get_root_dir
    >>> print("p = ", repr(get_root_dir()))  # doctest: +ELLIPSIS
    p = .../nubs')

    """
    # this folder is the root directory based on the location of this file (utils.py)
    return Path(__file__).resolve().parent


# %% Functions - main
def main() -> int:
    r"""Main function called when executed using the command line api."""
    # check for no command option
    command = sys.argv[1].lower() if len(sys.argv) >= 2 else "help"  # noqa: PLR2004
    # check for alternative forms of help with the base dcs command
    if command in {"help", "--help", "-h"}:
        try:
            return_code = print_help()
        except Exception:  # pylint: disable=broad-exception-caught  # noqa: BLE001
            return_code = _ReturnCodes.bad_help_file
    elif command in {"version", "--version", "-v"}:
        try:
            return_code = print_version()
        except Exception:  # pylint: disable=broad-exception-caught  # noqa: BLE001
            return_code = _ReturnCodes.bad_version
    elif command == "doctests":
        # determine if running in verbose mode
        verbose = "-v" in sys.argv[2:] or "--verbose" in sys.argv[2:]
        # initialize failure status
        had_failure = False
        # loop through and test each file
        folder = get_root_dir()
        files = folder.rglob("*.py")
        for file in files:
            failure_count, _ = doctest.testfile(str(file), report=True, verbose=verbose, module_relative=False)
            if failure_count > 0:
                had_failure = True
        return_code = _ReturnCodes.test_failures if had_failure else _ReturnCodes.clean
    elif command == "tests":
        # run tests using pytest
        import pytest  # pylint: disable=import-outside-toplevel  # noqa: PLC0415

        exit_code = pytest.main([str(get_root_dir() / "tests"), "-rfEsP"] + sys.argv[2:])  # noqa: RUF005
        return_code = _ReturnCodes.clean if exit_code == 0 else _ReturnCodes.test_failures
    else:
        print(f'Unknown command: "{command}"')
        return_code = _ReturnCodes.bad_command
    return sys.exit(return_code)


# %% Functions - print_help
def print_help(help_file: Path | None = None) -> int:
    r"""
    Prints the contents of the README.rst file.

    Returns
    -------
    return_code : int
        Return code for whether the help file was successfully loaded

    Examples
    --------
    >>> from nubs import print_help
    >>> print_help()  # doctest: +SKIP

    """
    if help_file is None:
        help_file = get_root_dir().parent.joinpath("README.rst")
    if not help_file.is_file():
        print(f'Warning: help file at "{help_file}" was not found.')
        return _ReturnCodes.bad_help_file
    with help_file.open(encoding="utf-8") as file:
        text = file.read()
    print(text)
    return _ReturnCodes.clean


# %% Functions - print_version
def print_version() -> int:
    r"""
    Prints the version of the library.

    Returns
    -------
    return_code : int
        Return code for whether the version was successfully read

    Examples
    --------
    >>> from nubs import print_version
    >>> print_version()  # doctest: +SKIP

    """
    try:
        version = ".".join(str(x) for x in version_info)
        return_code = _ReturnCodes.clean
    except Exception:  # pylint: disable=broad-exception-caught  # noqa: BLE001
        version = "unknown"
        return_code = _ReturnCodes.bad_version
    print(version)
    return return_code


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="nubs.tests.test_cli", exit=False)
    doctest.testmod(verbose=False)
