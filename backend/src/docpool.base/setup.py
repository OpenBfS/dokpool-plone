from setuptools import find_packages
from setuptools import setup


version = "2.1.0.dev0"

setup(
    name="docpool.base",
    version=version,
    description="",
    long_description="""\
""",
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="",
    author="Starzel.de for Bundesamt für Strahlenschutz",
    author_email="info@starzel.de",
    url="https://github.com/OpenBfS/dokpool-plone",
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["docpool"],
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.11",
    install_requires=[
        # -*- Extra requirements: -*-
        "setuptools",
        "collective.monkeypatcher",
        "docpool.config",
        "pypdf",
        "eea.facetednavigation",
        "collective.eeafaceted.z3ctable",
        "z3c.unconfigure",
        "collective.impersonate",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
