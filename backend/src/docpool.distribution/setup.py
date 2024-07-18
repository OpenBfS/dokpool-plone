"""Installer for the docpool.distribution package."""

from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
"""


setup(
    name="docpool.distribution",
    version="1.0.0a0",
    description="Example content for docpool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Distribution",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Philip Bauer",
    author_email="bauer@starzel.de",
    url="https://github.com/OpenBfS/dokpool-plone",
    project_urls={
        "Source": "https://github.com/OpenBfS/dokpool-plone",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["docpool"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Products.CMFPlone",
        "plone.api",
        "plone.distribution",
        "plone.exportimport",
    ],
    extras_require={},
    entry_points="""
    """,
)
