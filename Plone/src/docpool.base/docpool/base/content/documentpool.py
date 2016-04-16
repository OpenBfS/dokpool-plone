# -*- coding: utf-8 -*-
#
# File: documentpool.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DocumentPool content type. See documentpool.py for more
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

from plone.dexterity.content import Container

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.component import adapter
from zope.lifecycleevent import IObjectAddedEvent, IObjectRemovedEvent
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import parent
import random
from elan.policy.chomsky import chomsky
from loremipsum import get_paragraphs
from zope.event import notify
from docpool.base.events import DocumentPoolInitializedEvent,\
    DocumentPoolRemovedEvent
from docpool.base.structures import docPoolAdded as docPoolAddedExtern, docPoolRemoved as docPoolRemovedExtern
#from docpool.base.utils import _copyPaste, queryForObjects
from plone.app.textfield.value import RichTextValue
from plone.protect.auto import safeWrite
from docpool.base.content.doctype import IDocType
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IDocumentPool(form.Schema):
    """
    """
        
    prefix = schema.TextLine(
                        title=_(u'label_documentpool_prefix', default=u'Prefix names'),
                        description=_(u'description_documentpool_prefix', default=u'Will be used to construct user and group names. If left blank, the id of the ESD will be used. '),
                        required=False,
##code-section field_prefix
##/code-section field_prefix                           
    )
    

##code-section interface
##/code-section interface


class DocumentPool(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDocumentPool)
    
##code-section methods
    
    def configure(self):
        """
        """
        docPoolAdded(self, None)
        return self.restrictedTraverse("@@view")()
        
    def myPrefix(self):
        return self.prefix or self.getId()
    
    def reindexAll(self):  
        """
        """  
        cat = getToolByName(self, "portal_catalog")
        res = cat(path=self.dpSearchPath())
        for r in res:
            o = r.getObject()
            if o:
                o.reindexObject()
                o.reindexObjectSecurity()
                
    def myDocumentTypes(self, ids_only=False):
        """
        """
        cat = getToolByName(self, "portal_catalog")
        res = cat(path=self.dpSearchPath(),object_provides=IDocType.__identifier__,sort_on="getId")
        if ids_only:
            return [ dt.getId for dt in res ]
        else:
            return [ (dt.getId, dt.Title) for dt in res ]
        
    def correctAllDocTypes(self):
        """
        """
        # Correct references
        mpath = self.dpSearchPath()
        from docpool.base.utils import queryForObjects
        ecs = queryForObjects(self, path=mpath, portal_type="ELANDocCollection")
        for ec in ecs:
            ec.getObject().correctDocTypes() 

    def dpSearchPath(self):
        """
        """
        return "/".join(self.getPhysicalPath())
    

    def deleteText(self, obj):
        """
        """
        safeWrite(obj, self.REQUEST)
        obj.text = RichTextValue(u"", 'text/plain', 'text/html')
        
    def currentApplication(self):
        """
        """
        if shasattr(self, "myDPApplication", acquire=True):
            return self.myDPApplication().getId()
        else:
            return "elan"
        
##/code-section methods 

    def myDocumentPool(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getContentAreas(self, **kwargs):
        """
        """
        args = {'portal_type':'ContentArea'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getDPConfigs(self, **kwargs):
        """
        """
        args = {'portal_type':'DPConfig'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
@adapter(IDocumentPool, IObjectAddedEvent)
def docPoolAdded(obj, event=None):
    """
    """
    self = obj
    docPoolAddedExtern(obj, event)
    notify(DocumentPoolInitializedEvent(self))
 
@adapter(IDocumentPool, IObjectRemovedEvent)
def docPoolRemoved(obj, event=None):
    """
    """
    self = obj
    docPoolRemovedExtern(obj, event)
    notify(DocumentPoolRemovedEvent(self))


##/code-section bottom 
