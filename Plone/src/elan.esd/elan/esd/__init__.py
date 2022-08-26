from AccessControl import allow_module
from elan.esd import monkey  # noqa: F401
from plone import api
from zope.i18nmessageid import MessageFactory


DocpoolMessageFactory = MessageFactory("elan.esd")
allow_module("Products.CMFQuickInstallerTool.QuickInstallerTool")
allow_module("elan.esd")
allow_module("elan.esd.utils")
allow_module("elan.esd.portlets.recent")

api.__allow_access_to_unprotected_subobjects__ = 1
api.user.__allow_access_to_unprotected_subobjects__ = 1
api.group.__allow_access_to_unprotected_subobjects__ = 1
