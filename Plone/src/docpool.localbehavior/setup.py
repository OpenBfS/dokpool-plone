from setuptools import find_packages
from setuptools import setup

import os


version = "1.0"

setup(
    name="docpool.localbehavior",
    version=version,
    description="Local behavior support for Dexterity",
    long_description=open("README.txt").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=["Programming Language :: Python"],
    keywords="",
    author="",
    author_email="",
    url="",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["docpool"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
