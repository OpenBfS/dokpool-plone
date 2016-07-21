# -*- coding: utf-8 -*-
#
# File: elantransfers.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANTransfers content type. See elantransfers.py for more
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

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports

from elan.esd.config import PROJECTNAME

from elan.esd import DocpoolMessageFactory as _

class IELANTransfers(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class ELANTransfers(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANTransfers)
    
##code-section methods
##/code-section methods 

    def myELANTransfers(self):
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

    def getELANTransferFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANTransferFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom
