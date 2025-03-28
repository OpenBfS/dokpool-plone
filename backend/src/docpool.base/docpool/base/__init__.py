from AccessControl import allow_module
from plone import api
from plone.app.upgrade.utils import alias_module
from plone.namedfile.browser import DisplayFile
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)
DocpoolMessageFactory = MessageFactory("docpool.base")

from docpool.base import appregistration  # noqa: F401
from docpool.base import monkey  # noqa: F401


allow_module("docpool.base")
allow_module("docpool.base.config")
allow_module("docpool.base.utils")
api.__allow_access_to_unprotected_subobjects__ = 1
api.user.__allow_access_to_unprotected_subobjects__ = 1
api.group.__allow_access_to_unprotected_subobjects__ = 1


class IBBB(Interface):
    pass


alias_module("contentimport.interfaces.IContentimportLayer", IBBB)

if "text/html" not in DisplayFile.allowed_inline_mimetypes:
    DisplayFile.allowed_inline_mimetypes.append("text/html")
    logger.info(
        "Patch plone.namedfile.browser.DisplayFile to allow text/html to be displayed inline."
    )
