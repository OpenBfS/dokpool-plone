# -*- coding: utf-8 -*- 
from setuptools import setup, find_packages
import os

name = 'wsapi4plone.core'
version_txt = os.path.join('wsapi4plone', 'core', 'version.txt')
version = open(version_txt).read().strip()

DEV_STATES = [
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    ]

if version.find('a') >= 0:
    state = 0
elif version.find('b') >= 0:
    state = 1
else:
    state = 2
development_status = DEV_STATES[state]

def read(*path):
    return open(os.path.join(*path)).read()

setup(
    name=name,
    version=version,
    author='WebLion Group, Penn State University',
    author_email='support@weblion.psu.edu',
    description="A Web Services API for Plone (>=3.x).",
    long_description='\n\n'.join([read('README.txt'),
                                  ]),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        development_status,
        ],
    keywords='wsapi api xmlrpc weblion',
    url='http://packages.python.org/wsapi4plone.core/',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['wsapi4plone'],
    extras_require = dict(test=['zope.app.testing',
                                'zope.testing',
                                'zope.traversing',
                                ],
                          blob=['plone.app.blob'],
                          plone33=['collective.autopermission==1.0b2',
                                   'plone.app.blob==1.5',
                                   'ZODB3==3.8.3',
                                   ],
                          ),
    install_requires=['setuptools',
                      'collective.autopermission',
                      ##'Plone',
                      # We have support for plone.app.blob, but only use it
                      # when it's already available (e.g Plone >= 4).
                      ##'plone.app.blob',
                      ],
    entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone""",
    include_package_data=True,
    zip_safe=False,
    )
