#!/usr/bin/env python

VERSION = "2.1.11"

__authors__ = ["Soufiane Oualil", "Ahmed Bargady"]
__contact__ = "www.google.com"
__copyright__ = "Copyright 2022, AtlasSonic"
__credits__ = ["Soufinae Oualil"]
__date__ = "2023/07/17"
__deprecated__ = False
__email__ = "someone@um6p.ma"
__license__ = "MIT"
__maintainer__ = "developer"
__status__ = "Development"
__version__ = VERSION

import sys
import setuptools

if not sys.version_info >= (3, 7):
    sys.exit('Sorry, python3.7+ is required for this package')

setuptools.setup(
    name="sonic_engine",
    version=VERSION,
    author="Soufiane Oualil, Ahmed Bargady",
    description="Sonic Engine is a python package for the AtlasSonic project",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=["pyaml == 23.7.0", "redis == 4.2.2",
                      "numpy", "pytest", "yapsy", "flask"]
)
