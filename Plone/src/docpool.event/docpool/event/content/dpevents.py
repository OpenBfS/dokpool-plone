# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

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

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.interface.declarations import classImplements

from Products.CMFPlone.utils import parent
from logging import getLogger
logger = getLogger("dpevents")
##/code-section imports

from docpool.event import DocpoolMessageFactory as _

class IDPEvents(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class DPEvents(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPEvents)
    
##code-section methods

    def migrate(self):
        f = parent(self)
        if hasattr(self, '_setPortalTypeName'):
            self._setPortalTypeName("DPEvents")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPEvents
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

##/code-section methods

    def myDPEvents(self):
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

    def getDPEvents(self, **kwargs):
        """
        """
        args = {'portal_type':'DPEvent'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
class ELANScenarios(DPEvents):
    pass
##/code-section bottom
