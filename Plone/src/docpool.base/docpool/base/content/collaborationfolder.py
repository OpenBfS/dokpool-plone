# -*- coding: utf-8 -*-
#
# File: collaborationfolder.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the CollaborationFolder content type. See collaborationfolder.py for more
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
from docpool.base.content.simplefolder import SimpleFolder, ISimpleFolder

from Products.CMFCore.utils import getToolByName

##code-section imports
from zExceptions import BadRequest
from docpool.base.utils import getAllowedDocumentTypes, getAllowedDocumentTypesForGroup
from plone.api import user
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class ICollaborationFolder(form.Schema, ISimpleFolder):
    """
    """
        
    allowedPartnerDocTypes = schema.List(
                        title=_(u'label_collaborationfolder_allowedpartnerdoctypes', default=u'Document types allowed for the guest group(s)'),
                        description=_(u'description_collaborationfolder_allowedpartnerdoctypes', default=u''),
                        required=True,
##code-section field_allowedPartnerDocTypes
                        value_type=schema.Choice(source="docpool.base.vocabularies.GroupDocType"),
##/code-section field_allowedPartnerDocTypes                           
    )
    

##code-section interface
##/code-section interface


class CollaborationFolder(Container, SimpleFolder):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ICollaborationFolder)
    
##code-section methods
    def createActions(self):
        """
        """
        log("Creating Collaboration Folder")

        placeful_wf = getToolByName(self, 'portal_placeful_workflow')
        try:
            self.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        except BadRequest, e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = 'dp-collaboration-folder'
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.updateSecurity()
        self.reindexObjectSecurity()

    def customMenu(self, menu_items):
        """
        """
        print user.get_roles(obj=self)
        if not "Reviewer" in user.get_roles(obj=self):
            return SimpleFolder.customMenu(self, menu_items)
        else:
            print "Reviewer"
            dts = getAllowedDocumentTypesForGroup(self)
            filter = False
            if self.allowedPartnerDocTypes:
                print self.allowedPartnerDocTypes
                filter = True
            res = []
            for menu_item in menu_items:
                if menu_item.get('id') == 'DPDocument':
                    for dt in dts:
                        #print dt.id
                        if not dt.getObject().globalAllow: # only generally allowed doctypes
                            continue                        
                        if not filter or dt.id in self.allowedPartnerDocTypes:
                            res.append({'extra': 
             {'separator': None, 'id': dt.id, 'class': 'contenttype-%s' % dt.id}, 
                                        'submenu': None, 
                                        'description': '', 
                                        'title': dt.Title, 
                                        'action': '%s/++add++DPDocument?form.widgets.docType:list=%s' % (self.absolute_url(), dt.id), 
                                        'selected': False, 
                                        'id': dt.id, 
                                        'icon': None})
                else:
                    res.append(menu_item)
            return res
##/code-section methods 

    def myCollaborationFolder(self):
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

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
