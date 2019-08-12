# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='elan.journal',
      version=version,
      description="",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='German Federal Office for Radiation Protection',
      author_email='kprobst@bfs.de',
      url='http://www.bfs.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['elan'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'ftw.upgrade',
          'plone.api',
          'plone.app.dexterity',
          'plone.app.layout',
          'plone.app.textfield',
          'plone.batching',
          'plone.dexterity',
          'plone.memoize',
          'plone.namedfile [blobs]',
          'Products.CMFPlone >=4.3',
          'Products.GenericSetup',
          'setuptools',
          'zope.annotation',
          'zope.component',
          'zope.container',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

