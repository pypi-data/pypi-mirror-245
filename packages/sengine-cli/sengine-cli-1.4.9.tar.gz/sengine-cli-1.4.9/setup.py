#!/usr/bin/env python

VERSION = "1.4.9"

__authors__ = ["Soufiane Oualil", "Ahmed Bargady"]
__contact__ = "www.google.com"
__copyright__ = "Copyright 2023, AtlasSonic"
__credits__ = ["Soufinae Oualil"]
__date__ = "2023/12/07"
__deprecated__ = False
__email__ = "someone@um6p.ma"
__license__ = "MIT"
__maintainer__ = "developer"
__status__ = "Development"
__version__ = VERSION

from setuptools import setup, find_packages

setup(
    name="sengine-cli",
    version=VERSION,
    packages=find_packages(),
    author="Soufiane Oualil, Ahmed Bargady",
    description="S-Egnine CLI is a command line interface for the Sonic Engine extensions manager.",
    entry_points={"console_scripts": ["sengine-cli = sengine_cli.__main__:main"]},
    install_requires=["sonic-engine == 2.1.15"],
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    copyright=("2023, AtlasSonic"),
)
