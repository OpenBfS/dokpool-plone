# -*- coding: utf-8 -*-
#
# File: privatefolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the PrivateFolder content type. See privatefolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Container
from docpool.base.content.simplefolder import SimpleFolder, ISimpleFolder

from Products.CMFCore.utils import getToolByName

from zExceptions import BadRequest

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _


class IPrivateFolder(form.Schema, ISimpleFolder):
    """
    """


class PrivateFolder(Container, SimpleFolder):
    """
    """

    security = ClassSecurityInfo()

    implements(IPrivateFolder)

    def createActions(self):
        """
        """
        log("Creating Private Folder")

        placeful_wf = getToolByName(self, 'portal_placeful_workflow')
        try:
            self.manage_addProduct[
                'CMFPlacefulWorkflow'
            ].manage_addWorkflowPolicyConfig()
        except BadRequest, e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = 'dp-private-folder'
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.updateSecurity()
        self.reindexObjectSecurity()

    def myPrivateFolder(self):
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
        args = {'portal_type': 'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoDocuments(self, **kwargs):
        """
        """
        args = {'portal_type': 'InfoDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getPrivateFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'PrivateFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
