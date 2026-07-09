r"""
Test file for the `cli` module of the "nubs" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Adapted to nubs library by David C. Stauffer in July 2026.

"""

# %% Imports
import contextlib
import io
import unittest

import nubs as nubs


# %% main
class Test_main(unittest.TestCase):
    r"""
    Tests the main function with the following cases:
        TBD
    """

    pass  # TODO: write this  # noqa: PIE790


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
        self.assertTrue(output.startswith(("#######\nlmspace\n#######\n", "####\nnubs\n####\n")))

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
