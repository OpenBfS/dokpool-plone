# -*- coding: utf-8 -*-
"""Installer for the docpool.config package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='docpool.config',
    version='0.1',
    description="Configuration details for a deployment of the BfS Docpool application",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Henning Rietz',
    author_email='hr@condat.de',
    url='http://pypi.python.org/pypi/docpool.config',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['docpool'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'z3c.jbot'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
