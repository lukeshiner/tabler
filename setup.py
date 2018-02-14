#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='tabler',
    version='2.0',
    description='Simple interface for tabulated data and .csv files',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://tabler.lukeshiner.com',
    keywords=['table', 'csv', 'simple'],
    install_requires=['requests', 'ezodf', 'lxml', 'openpyxl', 'pyexcel_ods3'],
    packages=find_packages(),
    )
