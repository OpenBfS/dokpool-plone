# -*- coding: utf-8 -*-
"""Main product initializer
"""

from AccessControl import allow_class
from AccessControl import allow_module
from plone import api
from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
from zope.i18nmessageid import MessageFactory

from elan.esd import config
from six.moves import zip


allow_module("Products.CMFQuickInstallerTool.QuickInstallerTool")
allow_module("elan.esd")
allow_module("elan.esd.utils")
allow_module("elan.esd.portlets.recent")

api.__allow_access_to_unprotected_subobjects__ = 1
api.user.__allow_access_to_unprotected_subobjects__ = 1
api.group.__allow_access_to_unprotected_subobjects__ = 1

from elan.esd import monkey  # noqa: F401

# DocumentPool specific
# from monkeyDocumentPool import esdAdded, esdRemoved, configure
# from docpool.base.content.documentpool import DocumentPool, IDocumentPool
# import zope.component
# from zope.lifecycleevent import IObjectAddedEvent, IObjectRemovedEvent
# from Products.CMFCore.utils import getToolByName
#
# def check(self):
#     qi = getToolByName(self, 'portal_quickinstaller')
#     prods = qi.listInstallableProducts(skipInstalled=False)
#     for prod in prods:
#         if (prod['id'] == 'elan.esd') and (prod['status'] == 'installed'):
#             return 1
#     return 0
#
# if check():
#     gsm = zope.component.getGlobalSiteManager()
#     gsm.registerHandler(esdAdded, (IDocumentPool, IObjectAddedEvent))
#     gsm.registerHandler(esdRemoved, (IDocumentPool, IObjectRemovedEvent))
#
#     DocumentPool.configure = configure


# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

DocpoolMessageFactory = MessageFactory('elan.esd')
allow_class(DocpoolMessageFactory)


def initialize(context):
    """Intializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.

    """

    # Retrieve the content types that have been registered with Archetypes
    # This happens when the content type is imported and the registerType()
    # call in the content type's module is invoked. Actually, this happens
    # during ZCML processing, but we do it here again to be explicit. Of
    # course, even if we import the module several times, it is only run
    # once!

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME
    )

    # Now initialize all these content types. The initialization process takes
    # care of registering low-level Zope 2 factories, including the relevant
    # add-permission. These are listed in config.py. We use different
    # permisisons for each content type to allow maximum flexibility of who
    # can add which content types, where. The roles are set up in rolemap.xml
    # in the GenericSetup profile.

    for atype, constructor in zip(content_types, constructors):
        cmfutils.ContentInit(
            "%s: %s" % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
        ).initialize(context)
