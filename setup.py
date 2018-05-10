#!/usr/bin/env python

"""Setup for tabler package."""

from setuptools import find_packages, setup

setup(
    name='tabler',
    version='2.1',
    description='Simple interface for tabulated data and .csv files',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://tabler.lukeshiner.com',
    keywords=['table', 'csv', 'simple'],
    install_requires=[
        'requests', 'ezodf', 'lxml', 'openpyxl', 'pyexcel_ods3', 'jinja2'],
    packages=find_packages(),
    )
