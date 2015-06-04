# -*- coding: utf-8 -*-
#
# File: doctype.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DocType content type. See doctype.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.utils import queryForObjects, queryForObject, back_references
from Products.Archetypes.utils import DisplayList, shasattr
from z3c.relationfield.relation import RelationValue
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget
from zope.component import getUtility, adapter
from zope.intid.interfaces import IIntIds
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from plone.dexterity.interfaces import IEditFinishedEvent

# @grok.provider(IContextSourceBinder)
# def availableCategories(context):
#     if hasattr(context, "dpSearchPath"):
#         path = context.dpSearchPath() + "/esd"
#     else:
#         path = "/Plone/esd"
#     query = { "portal_type" : ["ELANDocCollection"],
#               "path": {'query' :path } 
#              }
# 
#     return ObjPathSourceBinder(navigation_tree_query = query,object_provides=IELANDocCollection.__identifier__).__call__(context) 
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IDocType(form.Schema):
    """
    """
        
    allowUploads = schema.Bool(
                        title=_(u'label_doctype_allowuploads', default=u'Can contain documents and images'),
                        description=_(u'description_doctype_allowuploads', default=u''),
                        required=False,
                        default=True,
##code-section field_allowUploads
##/code-section field_allowUploads                           
    )
    
        
    publishImmediately = schema.Bool(
                        title=_(u'label_doctype_publishimmediately', default=u'Publish immediately?'),
                        description=_(u'description_doctype_publishimmediately', default=u''),
                        required=False,
                        default=False,
##code-section field_publishImmediately
##/code-section field_publishImmediately                           
    )
    
    

##code-section interface
##/code-section interface


class DocType(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDocType)
    
##code-section methods
        
##/code-section methods 


##code-section bottom
@adapter(IDocType, IEditFinishedEvent)
def updated(obj, event=None):
    # Actually, a transfer folder should never allow a change of ESD.
    # But the permission level could have been changed. So we adapt
    # the read permissions for the sending ESD accordingly.
    log("DocType updated: %s" % str(obj))
    mpath = "/"
    if shasattr(obj, "dpSearchPath", acquire=True):
        mpath = obj.dpSearchPath()
    docs = queryForObjects(obj, path=mpath,docType=obj.getId())
    for doc in docs:
        try:
            doc.getObject().reindexObject()
        except:
            pass
##/code-section bottom 
