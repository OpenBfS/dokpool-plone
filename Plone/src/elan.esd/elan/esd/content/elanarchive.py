# -*- coding: utf-8 -*-
#
# File: elanarchive.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANArchive content type. See elanarchive.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import implements


class IELANArchive(form.Schema):
    """
    """


class ELANArchive(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(IELANArchive)

    APP = ELAN_APP

    def isSituationDisplay(self):
        """
        Marker for portlets
        """
        return 1

    def myELANArchive(self):
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
        args = {'portal_type': 'ContentArea'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getELANCurrentSituations(self, **kwargs):
        """
        """
        args = {'portal_type': 'ELANCurrentSituation'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
