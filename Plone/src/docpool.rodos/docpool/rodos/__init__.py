# -*- coding: utf-8 -*-
"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
from docpool.rodos import config

from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
from Products.CMFCore.permissions import setDefaultRoles

from AccessControl import allow_class

##code-section imports
##/code-section imports 

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

DocpoolMessageFactory = MessageFactory('docpool.rodos')
allow_class(DocpoolMessageFactory)

##code-section security
import appregistration
##/code-section security

def initialize(context):
    """Intializer called when used as a Zope 2 product.
    
    This is referenced from configure.zcml. Regstrations as a "Zope 2 product" 
    is necessary for GenericSetup profiles to work, for example.
    
    Here, we call the Archetypes machinery to register our content types 
    with Zope and the CMF.
    
    """
    ##code-section init
    ##/code-section init
    
    pass
    