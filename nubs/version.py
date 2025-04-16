r"""
File that acts as a sole-source for version history.

Notes
-----
#.  Written by David C. Stauffer in February 2022.
"""

# %% Constants
version_info = (1, 3, 0)

# Below is data about the minor release history for potential use in deprecating older support.
# For inspiration, see: https://numpy.org/neps/nep-0029-deprecation_policy.html

data = """Feb 22, 2022: nubs 0.9
Aug 10, 2022: nubs 1.0
Oct 26, 2023: nubs 1.1
Jan 24, 2024: nubs 1.2
Apr 16, 2025: nubs 1.3
"""

# Historical notes:
# v0.9 Initial release after splitting from the dstauffman library.
# v1.0 Official baseline release.
# v1.1 Official support Python v3.12, increment static tools like isort, mypy
# v1.2 Use newer typing standards from Python v3.10+
# v1.3 Ditch poetry entirely, use setuptools (and uv instead)
