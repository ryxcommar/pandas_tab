#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup
from setuptools import find_packages


def get_version(package):
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="pandas_tab",
    python_requires=">=3.7",
    version=get_version("pandas_tab"),
    license="MIT",
    description="Data exploration done quick.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="ryxcommar",
    author_email="ryxcommar@gmail.com",
    url="https://github.com/ryxcommar/pandas_tab",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": {
            "pandas_tab = pandas_tab.cli:cli"
        }
    },
    install_requires=[
        "pandas>=0.23.0",
        "click"
    ],
    extras_require={
        "full": [
            "jinja2",
            "IPython"
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Plugins",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
