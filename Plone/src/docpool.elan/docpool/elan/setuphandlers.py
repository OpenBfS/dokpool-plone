from plone import api
from zope.globalrequest import getRequest


def post_install(context):
    # Add additional setup code here
    from docpool.config.general.elan import install

    install(api.portal.get())

    catalog = api.portal.get_tool("portal_catalog")
    catalog.reindexIndex(["scenarios", "category"], REQUEST=getRequest())


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
