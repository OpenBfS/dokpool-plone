# -*- coding: utf-8 -*-
"""Main product initializer
"""

from AccessControl import allow_class
from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory


allow_module("docpool.elan.config")

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

DocpoolMessageFactory = MessageFactory('docpool.elan')
allow_class(DocpoolMessageFactory)

import appregistration  # noqa: F401


def initialize(context):
    """Intializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.

    """
