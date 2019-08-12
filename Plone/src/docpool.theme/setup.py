from setuptools import find_packages
from setuptools import setup

import os


version = '1.0'

setup(
    name='docpool.theme',
    version=version,
    description="DocPool Theme",
    long_description=open("README.txt").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='',
    author_email='',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['docpool'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'z3c.jbot',
        # -*- Extra requirements: -*-
        'docpool.menu',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
