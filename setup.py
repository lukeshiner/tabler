#!/usr/bin/env python
"""Setup for tabler package."""

import os

import setuptools

with open("README.rst", "r") as readme:
    long_description = readme.read()

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "tabler", "__version__.py"), "r") as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    keywords=["table", "csv", "simple"],
    install_requires=["requests", "pyexcel_ods", "openpyxl", "odswriter", "jinja2"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.5.0",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Other/Nonlisted Topic",
    ],
)
