# -*- coding: utf-8 -*-
#
# File: srphase.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRPhase content type. See srphase.py for more
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

from zope.component import adapter
from plone.dexterity.interfaces import IEditFinishedEvent

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

class ISRPhase(form.Schema):
    """
    """



class SRPhase(Container):
    """
    """
    security = ClassSecurityInfo()

    implements(ISRPhase)

    def getSRPhaseNames(self):
        """
        Index method
        """
        return [ self.getId() ]

    def getSRPhaseRefs(self):
        """
        Index method
        """
        return [ self.UID() ]

    def getPhaseTitle(self):
        """
        """
        return u"%s: %s" % (self.mySRScenario().Title().decode('utf-8'), self.Title().decode('utf-8'))


    def availableModuleConfigs(self):
        mtypes = self.modTypes()
        res = {}
        for mt in mtypes:
            res[mt[0]] = None
        mcs = self.getSRModuleConfigs()
        for mc in mcs:
            res[mc.modType] = mc
        return res



    def mySRPhase(self):
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

    def getSRModuleConfigs(self, **kwargs):
        """
        """
        args = {'portal_type':'SRModuleConfig'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(ISRPhase, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRPhase updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat._reindexObject(obj)
