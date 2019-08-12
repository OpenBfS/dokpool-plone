from setuptools import find_packages
from setuptools import setup

import os


version = '1.0'

setup(
    name='elan.theme',
    version=version,
    description="ELAN-E Theme for Plone 4",
    long_description=open("README.txt").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Framework :: Plone", "Programming Language :: Python"],
    keywords='',
    author='BfS',
    author_email='elan-e@bfs.de',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['elan'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'quintagroup.dropdownmenu',
    ],
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
