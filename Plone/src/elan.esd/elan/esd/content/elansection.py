# -*- coding: utf-8 -*-
#
# File: elansection.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANSection content type. See elansection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANSection(model.Schema):
    """
    """


@implementer(IELANSection)
class ELANSection(Container):
    """
    """

    security = ClassSecurityInfo()

    def myELANSection(self):
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

    def getDashboardCollections(self, **kwargs):
        """
        """
        args = {'portal_type': 'DashboardCollection'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getELANDocCollections(self, **kwargs):
        """
        """
        args = {'portal_type': 'ELANDocCollection'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRCollections(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRCollection'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
