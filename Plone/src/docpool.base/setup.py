# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.8.0.dev0'

setup(
    name='docpool.base',
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
    author='Condat AG',
    author_email='hr@condat.de',
    url='http://www.condat.de',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['docpool'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        # -*- Extra requirements: -*-
        'setuptools',
        'Products.CMFPlacefulWorkflow',
        'plone.app.dexterity [relations]',
        'collective.autopermission',
        'plone.namedfile [blobs]',
        'collective.dexteritytextindexer',
        'plone.app.contenttypes',
        'plone.app.relationfield',
        'plone.api',
        'plone.formwidget.querystring',
        'collective.monkeypatcher',
        'Products.CMFPlacefulWorkflow',
        'docpool.users',
        'docpool.localbehavior',
        'PyPDF2',
        'xhtml2pdf',
        'Products.CMFPlacefulWorkflow',
        'eea.facetednavigation',
        'Products.ATContentTypes',  # needed for some tests until we upgrade to 5.2
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
