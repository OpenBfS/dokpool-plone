# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.1'

setup(
    name='docpool.policy',
    version=version,
    description="",
    long_description="",
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Condat AG',
    author_email='hr@condat.de',
    url='http://xservice.condat.de/vportal/elan-e',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['docpool'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.app.caching',
        'plone.app.upgrade',
        'plone.formwidget.contenttree',
        'docpool.theme',
        'docpool.base',
        'docpool.transfers',
        'docpool.users',
        'docpool.config',
        'docpool.video',
        'docpool.caching',
        'docpool.dbaccess',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone      
      """,
)
