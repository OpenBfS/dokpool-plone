from setuptools import find_packages
from setuptools import setup


version = "2.0.0.dev0"

setup(
    name="docpool.base",
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
    keywords="",
    author="Condat AG",
    author_email="hr@condat.de",
    url="http://www.condat.de",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["docpool"],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        # -*- Extra requirements: -*-
        "setuptools",
        "collective.monkeypatcher",
        "docpool.config",
        "pypdf",
        "eea.facetednavigation",
        "collective.eeafaceted.z3ctable",
        "z3c.unconfigure",
        "Products.CMFFormController",
        "collective.impersonate",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      update_locale_docpoolbase = docpool.base.locales.update:update_locale
      """,
)
