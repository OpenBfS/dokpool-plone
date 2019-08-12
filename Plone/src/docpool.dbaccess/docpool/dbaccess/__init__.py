# -*- coding: utf-8 -*-
"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
from docpool.dbaccess import config

from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
from Products.CMFCore.permissions import setDefaultRoles

from AccessControl import allow_class

from AccessControl import allow_module

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

DocpoolMessageFactory = MessageFactory('docpool.dbaccess')
allow_class(DocpoolMessageFactory)

from docpool.dbaccess.content.errors import ObjectDuplicateException

allow_class(ObjectDuplicateException)
allow_module("docpool.dbaccess")
allow_module("docpool.dbaccess.utils")


def initialize(context):
    """Intializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.

    """

    pass
