# -*- coding: utf-8 -*-
#
# File: elaninfos.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANInfos content type. See elaninfos.py for more
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
from docpool.base.content.infofolder import InfoFolder, IInfoFolder

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.component import adapter
from zope.lifecycleevent import IObjectAddedEvent, IObjectRemovedEvent
##/code-section imports 

from elan.esd.config import PROJECTNAME

from elan.esd import ELAN_EMessageFactory as _

class IELANInfos(form.Schema, IInfoFolder):
    """
    """

##code-section interface
##/code-section interface


class ELANInfos(Container, InfoFolder):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANInfos)
    
##code-section methods
##/code-section methods 

    def myELANInfos(self):
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

    def getInfoDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getInfoFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getInfoFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getInfoLinks(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoLink'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
@adapter(IELANInfos, IObjectAddedEvent)
def infosAdded(obj, event=None):
    """
    Set local role for Content Administrators
    """
    print "infosAdded"
    self = obj
    esd = self.myDocumentPool()
    prefix = esd.prefix or esd.getId()
    prefix = str(prefix)
    self.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["Reviewer"])
    
    
##/code-section bottom 
