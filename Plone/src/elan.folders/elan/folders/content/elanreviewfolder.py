# -*- coding: utf-8 -*-
#
# File: elanreviewfolder.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANReviewFolder content type. See elanreviewfolder.py for more
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
from elan.esd.content.elanfolder import ELANFolder, IELANFolder

from Products.CMFCore.utils import getToolByName

##code-section imports
from zExceptions import BadRequest
##/code-section imports 

from elan.folders.config import PROJECTNAME

from elan.folders import ELAN_EMessageFactory as _

class IELANReviewFolder(form.Schema, IELANFolder):
    """
    """

##code-section interface
##/code-section interface


class ELANReviewFolder(Container, ELANFolder):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANReviewFolder)
    
##code-section methods
    def createActions(self):
        """
        """
        log("Creating Review Folder")
        placeful_wf = getToolByName(self, 'portal_placeful_workflow')
        try:
            self.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        except BadRequest, e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = 'elan-review-folder'
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.updateSecurity()
        self.reindexObjectSecurity()        

##/code-section methods 

    def myELANReviewFolder(self):
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

    def getELANDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getELANReviewFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANReviewFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
