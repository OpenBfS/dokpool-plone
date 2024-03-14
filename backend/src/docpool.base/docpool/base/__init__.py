from AccessControl import allow_module
from plone import api
from zope.i18nmessageid import MessageFactory

import logging
import pkg_resources


logger = logging.getLogger(__name__)
DocpoolMessageFactory = MessageFactory("docpool.base")

# TODO: Remove when https://community.plone.org/t/plone-6-beta-1-released/15485/5 is fixed
from docpool.base import appregistration  # noqa: F401
from docpool.base import expressions  # noqa
from docpool.base import monkey  # noqa: F401


allow_module("docpool.base")
allow_module("docpool.base.config")
allow_module("docpool.base.utils")
api.__allow_access_to_unprotected_subobjects__ = 1
api.user.__allow_access_to_unprotected_subobjects__ = 1
api.group.__allow_access_to_unprotected_subobjects__ = 1

# Patch Products.PloneHotfix20210518 to allow text/html to be displayed inline.
# TODO: Apply change to Plone 6 that does not have the HotFix
try:
    pkg_resources.get_distribution("Products.PloneHotfix20210518")
except pkg_resources.DistributionNotFound:
    pass
else:
    from plone.namedfile.browser import DisplayFile

    if "text/html" not in DisplayFile.allowed_inline_mimetypes:
        DisplayFile.allowed_inline_mimetypes.append("text/html")
        assert "application/pdf" in DisplayFile.allowed_inline_mimetypes
        logger.info(
            "Patch Products.PloneHotfix20210518 to allow text/html to be displayed inline."
        )