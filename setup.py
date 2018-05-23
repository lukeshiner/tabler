#!/usr/bin/env python

"""Setup for tabler package."""

import setuptools

with open("README.rst", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="tabler",
    version="2.1.2",
    description="Simple interface for tabulated data and .csv files",
    long_description=long_description,
    url="https://github.com/axevalley/tabler.git",
    author="Luke Shiner",
    author_email="luke@lukeshiner.com",
    keywords=["table", "csv", "simple"],
    install_requires=[
        "requests", "ezodf", "lxml", "openpyxl", "pyexcel_ods3", "jinja2"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>3.6.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"],
    )
