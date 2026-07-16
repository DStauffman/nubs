r"""
Test file for the `cli` module of the "nubs" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to nubs library by David C. Stauffer in July 2026.

"""

# %% Imports
import contextlib
import inspect
import io
import os
import pathlib
import unittest
from unittest.mock import patch

import nubs as nubs


# %% get_root_dir
class Test_get_root_dir(unittest.TestCase):
    r"""
    Tests the get_root_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        filepath = inspect.getfile(nubs.get_root_dir.__wrapped__)
        expected_root = pathlib.Path(os.path.split(filepath)[0])
        folder = nubs.get_root_dir()
        self.assertEqual(folder, expected_root)
        self.assertTrue(folder.is_dir())


# %% main
class Test_main(unittest.TestCase):
    r"""
    Tests the main function with the following cases:
        Help (good and bad)
        Version (good and bad)
        Doctests (pass and fail)
        Unit Tests (pass and fail)
    """

    def test_help(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), patch("sys.argv", ["name.py", "help"]), self.assertRaises(SystemExit) as exc:
            nubs.main()
        output = buffer.getvalue()
        buffer.close()
        self.assertEqual(exc.exception.code, 0)
        self.assertTrue(output.startswith("####\nnubs\n####\n"))

    def test_bad_help(self) -> None:
        with (
            patch("nubs.cli.print_help", return_value=nubs.cli._ReturnCodes.bad_help_file),  # noqa: SLF001
            patch("sys.argv", ["name.py", "--help"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 3)

    def test_version(self) -> None:
        buffer = io.StringIO()
        with (
            contextlib.redirect_stdout(buffer),
            patch("sys.argv", ["name.py", "version"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        output = buffer.getvalue()
        buffer.close()
        self.assertEqual(exc.exception.code, 0)
        self.assertIn(".", output)

    def test_bad_version(self) -> None:
        with (
            patch("nubs.cli.print_version", return_value=nubs.cli._ReturnCodes.bad_version),  # noqa: SLF001
            patch("sys.argv", ["name.py", "--version"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 4)

    def test_doctests(self) -> None:
        with (
            patch("nubs.cli.doctest.testfile", return_value=(0, "")) as mock_tester,
            patch("sys.argv", ["name.py", "doctests", "-v"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 0)
        mock_tester.assert_any_call(str(nubs.get_root_dir().joinpath("cli.py")), report=True, verbose=True, module_relative=False)  # fmt: skip

    def test_doctest_fails(self) -> None:
        with (
            patch("nubs.cli.doctest.testfile", return_value=(1, "")) as mock_tester,
            patch("sys.argv", ["name.py", "doctests"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 5)
        mock_tester.assert_any_call(str(nubs.get_root_dir().joinpath("cli.py")), report=True, verbose=False, module_relative=False)  # fmt: skip

    def test_unittests(self) -> None:
        with (
            patch("pytest.main", return_value=0) as mock_tester,
            patch("sys.argv", ["name.py", "tests"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 0)
        mock_tester.assert_called_with([str(nubs.get_root_dir().joinpath("tests")), "-rfEsP"])

    def test_bad_unittests(self) -> None:
        with (
            patch("pytest.main", return_value=-1) as mock_tester,
            patch("sys.argv", ["name.py", "tests", "--extra"]),
            self.assertRaises(SystemExit) as exc,
        ):
            nubs.main()
        self.assertEqual(exc.exception.code, 5)
        mock_tester.assert_called_with([str(nubs.get_root_dir().joinpath("tests")), "-rfEsP", "--extra"])


# %% print_help
class Test_print_help(unittest.TestCase):
    r"""
    Tests the print_help function with the following cases:
        Nominal
        Specified file
    """

    def test_nominal(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            nubs.print_help()
        output = buffer.getvalue()
        buffer.close()
        self.assertTrue(output.startswith("####\nnubs\n####\n"))

    def test_specify_file(self) -> None:
        help_file = nubs.get_root_dir().joinpath("tests", "test_cli.py")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            nubs.print_help(help_file)
        output = buffer.getvalue()
        buffer.close()
        self.assertTrue(output.startswith('r"""\nTest file for the `cli` module'))


# %% print_version
class Test_print_version(unittest.TestCase):
    r"""
    Tests the print_version function with the following cases:
        Nominal
    """

    def test_nominal(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            nubs.print_version()
        output = buffer.getvalue()
        buffer.close()
        self.assertIn(".", output)


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
