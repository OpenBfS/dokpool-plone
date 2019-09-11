# -*- coding: utf-8 -*-
#
# File: elanarchives.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANArchives content type. See elanarchives.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANArchives(model.Schema):
    """
    """


@implementer(IELANArchives)
class ELANArchives(Container):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def isSituationDisplay(self):
        """
        Marker for portlets
        """
        return 0

    def myELANArchives(self):
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

    def getELANArchives(self, **kwargs):
        """
        """
        args = {'portal_type': 'ELANArchive'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
