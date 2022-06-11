from setuptools import find_packages, setup

version = "1.1"

setup(
    name="elan.policy",
    version=version,
    description="",
    long_description="",
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="",
    author="Condat AG",
    author_email="hr@condat.de",
    url="http://xservice.condat.de/vportal/elan-e",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["elan"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "Products.CMFPlacefulWorkflow",
        "plone.app.caching",
        "plone.app.upgrade",
        "docpool.theme",
        "docpool.base",
        "docpool.users",
        "docpool.config",
        "docpool.dashboard",
        "docpool.video",
        "docpool.caching",
        "docpool.elan",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
