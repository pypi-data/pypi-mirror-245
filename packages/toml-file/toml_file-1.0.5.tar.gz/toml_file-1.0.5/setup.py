#!/usr/bin/env python
"""
Python distutils setup.py script:

Usage:
------

 * Recommended: Install via pip / pypi for the latest version *
 
    $ pip install toml_file
 
 
Install as a python package [not manual uninstall will be required]
    $ python setup.py install

Make a wheel and isntall [pip install wheel]
    $ python setup.py sdist bdist_wheel
    $ pip install wheel_file.whl
    
Upload to pypi [requires authorisation]
    $ setup.py upload

editable install
pip install -e /path/to/package
"""
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

import toml_file

#-------------------------------------------------------------------------------
# Add useful commands
#-------------------------------------------------------------------------------
class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds")
            here = os.path.abspath(os.path.dirname(__file__))
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution")
        os.system('"{}" setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine")
        os.system("twine upload dist//*")

        sys.exit()
        
#-------------------------------------------------------------------------------
# Collect data for the distutils setup() call.
#-------------------------------------------------------------------------------

# Package meta-data.
NAME = "toml_file"
DESCRIPTION = "TOML file reader - python module to read/write toml configuration files"
URL = "https://gitlab.com/tcharrett/toml_file"
EMAIL = "tcharrett@gmail.com"
AUTHOR = "Tom Charrett"
REQUIRES_PYTHON = ">=3.7.6"
VERSION = toml_file.__version__

# What packages are required for this module to be executed?
REQUIRED = []

# What packages are optional?
EXTRAS = {}

LONG_DESCRIP = """
TOML file reader - python module to read/write toml configuration files

- Files can be loaded and saved completed with comments and formating
- Configuration files can be templated and values validated on load or value changes

Two interaces:

Simple dictionaries {key: value} 
    - data dictionary with nested dictionary with {key: value}
    - template dictionary with comments/type information
    - template allows type, min/max  and other validators to be set and stores 
      comments
    - use load/save functions to open/save to file.

Config object interface:
    - allows seamless use of template/data via custom dictlike interface
    - use cfg = Config(filename) to open
    - access subtables/keys via exteneded key indexing e.g. cfg['Table1.subtable.key'] = 1
    - if a template has been set any value will be validated when it is set.
    - if a template has been set any missing values will return the defualt and be created.
    - use cfg.save(filename) to save
"""

#Find packages to install
PACKAGES = find_packages()

#-------------------------------------------------------------------------------
#Do the setup call
#-------------------------------------------------------------------------------
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIP,
    author = AUTHOR,
    author_email = EMAIL,
    url = URL,
    packages = PACKAGES,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing",],
    #upload command
    cmdclass={"upload": UploadCommand},
)
